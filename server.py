import socket
from threading import Thread

def clientthread(conn,addr,nickname):
    conn.send('Welcome to this chatroom!'.encode('utf-8'))
    while(True):
        try:
            message = conn.recv(2048).decode('utf-8')
            if(message):
                print(message)
                broadcast(message,conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue
def broadcast(message,conn):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            remove(client)
def remove(object):
    if(object in clients):
        clients.remove(object)
        
def remove_nickname(nickname):
    if(nickname in nicks):
        nicks.remove(nickname)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address,port))
server.listen()

clients = []
nicks = []
print('Server is live')

while(True):
    conn,addr = server.accept()
    nickname = conn.recv(2048).decode('utf-8')
    clients.append(conn)
    nicks.append(nickname)
    msg = '{} joined'.format(nickname)
    print(msg)
    broadcast(msg,conn)
    print(addr[0],'connected')
    new_thread = Thread(target=clientthread,args=(conn,addr,nickname))
    new_thread.start()