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
        self.Window.withdraw()
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
						command = lambda: self.goAhead(self.nameEntry.get()))
        self.go.place(relx=0.4,rely=0.55)
        self.login.mainloop()
        
    def goAhead(self,name):
        self.login.destroy()
        rcv = Thread(target=self.receive)
        rcv.start()
        self.createChatWindow(name)

    def receive(self):
        while(True):
            try:
                response = client.recv(2048).decode('utf-8')
                if(response.split(':')[0].strip()==self.name):
                    pass
                else:
                    # print(response)
                    self.show_received_message(response)
            except:
                # print('Failed to fetch response')
                client.close()
                break
    def createChatWindow(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title('CHATROOM')
        self.line = Label(self.Window,width=450,bg='#abb2b9')
        self.line.place(relwidth=1,rely=0.07,relheight=0.01)
        self.Window.resizable(width=False,height=False)
        self.Window.configure(width=470,height=550,bg='lightgrey')
        self.labelHead = Label(self.Window,text=('Welcome '+self.name),fg='blue',bg='white',font=('Helvetica',16))
        self.labelHead.place(relwidth=1)
        self.textCons = Text(self.Window,width=20,height=2,bg='#17202a',fg='#eaecee',font=('Helvetica',14),padx=5,pady=5)
        self.textCons.place(relheight=0.745,relwidth=1,rely=0.08)
        self.labelBottom = Label(self.Window,bg='#abb2b9',height=80)
        self.labelBottom.place(relwidth=1,rely=0.825)
        self.enterMessage = Entry(self.labelBottom,bg='#2c3e50',fg='#eaecee',font=('Helvetica',13))
        self.enterMessage.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.enterMessage.focus()
        self.sendButton = Button(self.labelBottom,text='Send',font=('Helvetica',13,'bold'),width=20,bg='#abb2b9',command=lambda:self.sendMessage(self.enterMessage.get()))
        self.sendButton.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)
        self.textCons.config(cursor='arrow')
        scrollBar = Scrollbar(self.textCons)
        scrollBar.place(relheight=1,relx=0.974)
        scrollBar.config(command=self.textCons.yview())
        
    def sendMessage(self,message):
        self.textCons.config(state=DISABLED)
        self.message = message
        self.enterMessage.delete(0,END)
        send = Thread(target=self.show_message(message))
        send.start()
    
    def show_message(self,message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,message+'\n\n')
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
        self.textCons.config(state=DISABLED)
        self.write()
    
    def show_received_message(self,message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,message+'\n\n')
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
    
    def write(self):
        self.textCons.config(state=DISABLED)
        message = (f"{self.name}: {self.message}")
        client.send(message.encode('utf-8'))
        

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