import socket
from threading import Thread

nick = input('Please enter a nickname: ')

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000
client.connect((ip_address,port))
print('connected')

def receive():
    while(True):
        try:
            response = client.recv(2048).decode('utf-8')
            if(response.split(':')[0].strip()==nick):
                pass
            else:
                print(response)
        except:
            print('Failed to fetch response')
            client.close()
            break

def write():
    try:
        client.send(nick.encode('utf-8'))
    except:
        print('Setup failed')
        client.close()
    while(True):
        msg = '{} : {}'.format(nick,input(''))
        try:
            client.send(msg.encode('utf-8'))
        except:
            print('Failed to send message')
            client.close()

receive_thread = Thread(target=receive)
receive_thread.start()
write_thread = Thread(target=write)
write_thread.start()