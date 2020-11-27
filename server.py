# Manoela Werneck 95664
# Matheus Ximenes 95666

import socket
import threading
import os

HOST = ''
PORT = 20000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
        f.write(data)   # enquanto houver dados a receber, escreve os dados no arquivo
    f.close()
    print("Arquivo recebido.")

    return

def sendFile(con, name):
    error = ''
    try:
        f = open(name,'rb')
        for msg in f.readlines():   # enquanto houver dados, le e escreve no arquivo
            con.send(msg)
        f.close()
        print('Arquivo enviado.')
    except FileNotFoundError:
        error = 'INFO:Esse arquivo não está disponível'
        print('Arquivo indisponível')

    return error

# funcao que executa uma acao conforme o protocolo
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
            text = 'INFO:' + clients[client] + ' enviou ' + msg[1]
            forwardMessage(text, client)
            con.close()

        elif msg[0] == 'GET':
            con, clientTCP = tcp.accept()
            text = sendFile(con, msg[1])
            if len(text):
                udp.sendto(text.encode(), client) # se a funcao retornar texto de erro envia para o cliente
            con.close()

        elif msg[0] == 'BYE':
            text = 'INFO:' + clients[client] + ' saiu'
            forwardMessage(text, client)
            del clients[client] # remove de clientes conectados
            udp.sendto('INFO:disconnect'.encode(), client) # envia msg de controle para quem saiu parar de ouvir o servidor

        if len(clients) == 0:
            break

    tcp.close()
    return

t1 = threading.Thread(target=receive, args=())
t1.start()




