import socket
from threading import Thread

def clientthread(conn,addr):
    conn.send('Welcome to this chatroom!'.encode('utf-8'))
    while(True):
        try:
            message = conn.receive(2048).decode('utf-8')
            if(message):
                print('<'+addr[0]+'>'+message)
                broadcast(message,conn)
            else:
                remove(conn)
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

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address,port))
server.listen()

clients = []
print('Server is live')
while(True):
    conn,addr = server.accept()
    clients.append(conn)
    print(addr[0],'connected')
    new_thread = Thread(target=clientthread,args=(conn,addr))
    new_thread.start()