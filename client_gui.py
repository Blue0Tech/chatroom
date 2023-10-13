import socket
from threading import Thread
from tkinter import *

# nick = input('Please enter a nickname: ')

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = '192.168.1.247'
port = 8001
client.connect((ip_address,port))
print('connected')

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.login = Toplevel()
        self.login.title = 'Login'
        self.login.resizable(width=False,height=False)
        self.login.config(width=400,height=300)
        self.pls = Label(self.login,text='Please login to continue',justify='center',font=('Helvetica',14,'bold'))
        self.pls.place(relheight=0.15,relx=0.2,rely=0.07)
        self.nameLabel = Label(self.login,text='Name',font=('Helvetica',12))
        self.nameLabel.place(relheight=0.2,relx=0.1,rely=0.2)
        self.nameEntry = Entry(self.login,text='')
        self.nameEntry.focus()
        self.nameEntry.place(relheight=0.15,relx=0.4,rely=0.2)
        self.go = Button(self.login,
						text = "CONTINUE",
						font = "Helvetica 14 bold",
						command = lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4,rely=0.55)
        
    def goAhead(self,name):
        self.login.destroy()
        self.name = name
        rcv = Thread(target=self.receive)
        rcv.start()

    def receive(self):
        while(True):
            try:
                response = client.recv(2048).decode('utf-8')
                if(response.split(':')[0].strip()==self.name):
                    pass
                else:
                    print(response)
            except:
                print('Failed to fetch response')
                client.close()
                break


gui = GUI()

# def receive():
#     while(True):
#         try:
#             response = client.recv(2048).decode('utf-8')
#             if(response.split(':')[0].strip()==nick):
#                 pass
#             else:
#                 print(response)
#         except:
#             print('Failed to fetch response')
#             client.close()
#             break

# def write():
#     try:
#         client.send(nick.encode('utf-8'))
#     except:
#         print('Setup failed')
#         client.close()
#     while(True):
#         msg = '{} : {}'.format(nick,input(''))
#         try:
#             client.send(msg.encode('utf-8'))
#         except:
#             print('Failed to send message')
#             client.close()

# receive_thread = Thread(target=receive)
# receive_thread.start()
# write_thread = Thread(target=write)
# write_thread.start()