import socket
import threading

HOST = ''
PORT = 20000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp.bind((HOST, PORT))

clients = {}    # guarda tupla (IP, porta) e nome de clientes ativos no momento

def forwardMessage(msg, client):
    for client_socket in clients: # para todo cliente ativo
        if client_socket != client: # exceto para o cliente que enviou a msg
            udp.sendto(msg.encode(), client_socket) # envia msg

def receiveFile(con, name):
    f = open(name,'wb')
    while True:
        data = con.recv(1024)
        if not data:
            break
        f.write(data)
    f.close()

    return

def sendFile(con, name):
    f = open(name,'rb')
    for msg in f.readlines():
        con.send(msg)
    f.close()

    return

def receive():
    while True:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp.bind((HOST, PORT))
        tcp.listen(1)

        msg, client = udp.recvfrom(1024)
        msg = msg.decode().split(":")

        if msg[0] == 'USER':
            clients[client] = msg[1] # adiciona em clientes conectados
            text = 'INFO:' + msg[1] + ' entrou'
            forwardMessage(text, client)

        elif msg[0] == 'MSG':
            text = "MSG:" + clients[client] + ":" + msg[1]
            forwardMessage(text, client)

        elif msg[0] == 'LIST':
            print("Enviando lista de clientes ativos.")
            text = 'INFO:Online:\n'
            for client_socket in clients: # todos os clientes conectados
                text += clients[client_socket] + ", "
            udp.sendto(text.encode(), client) # envia apenas para quem pediu a lista

        elif msg[0] == 'FILE':
            con, clientTCP = tcp.accept()
            receiveFile(con, msg[1])
            print("Arquivo recebido.")
            text = 'INFO:' + clients[client] + ' enviou ' + msg[1]
            forwardMessage(text, client)
            con.close()

        elif msg[0] == 'GET':
            con, clientTCP = tcp.accept()
            sendFile(con, msg[1])
            print('Arquivo enviado.')
            con.close()

        elif msg[0] == 'BYE':
            text = 'INFO:' + clients[client] + ' saiu'
            forwardMessage(text, client)
            del clients[client] # remove de clientes conectados
            udp.sendto('INFO:disconnect'.encode(), client) # envia msg de controle para quem pediu pra sair para de ouvir o servidor

    tcp.close()
    return

t1 = threading.Thread(target=receive, args=())
t1.start()




