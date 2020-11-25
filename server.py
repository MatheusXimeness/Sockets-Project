import socket
import threading

HOST = ''
PORT = 20000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp.bind((HOST, PORT))

clients = {}    # guarda tupla (IP, porta) e nome de clientes ativos no momento

def forwardMessage(msg, client):
    for client_socket in clients: # para todo cliente ativo
        if client_socket != client: # exceto para o cliente que enviou a msg
            udp.sendto(msg.encode(), client_socket) # envia msg


def receive():

    while True:
        msg, client = udp.recvfrom(1024)
        msg = msg.decode().split(":")
        print(msg)
        if msg[0] == 'USER':
            clients[client] = msg[1] # adiciona em clientes conectados
            text = 'INFO:' + msg[1] + ' entrou'
            forwardMessage(text, client)
        elif msg[0] == 'MSG':
            text = "MSG:" + clients[client] + ":" + msg[1]
            forwardMessage(text, client)
        elif msg[0] == 'LIST':
            print("Encaminhando lista...")
            text = 'Online:\n'
            for client_socket in clients: # todos os clientes conectados
                text += clients[client_socket] + ", "
            udp.sendto(text.encode(), client) # envia apenas para quem pediu a lista
        elif msg[0] == 'FILE':
            # ...
            text = 'INFO:' + clients[client] + ' enviou '
            forwardMessage(text, client)
        elif msg[0] == 'GET':
            #...
            print('get')
        elif msg[0] == 'BYE':
            text = 'INFO:' + clients[client] + ' saiu'
            forwardMessage(text, client)
            del clients[client] # remove de clientes conectados

    return

t = threading.Thread(target=receive, args=())
t.start()

# udp.close()

# while True:
#     print('esperando...')
#     msg, client = udp.recvfrom(1024)
#     print(client, msg.decode())
#     udp.sendto('ack'.encode(), client)

# tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# tcp.bind((HOST, PORT))

# tcp.listen(1)




