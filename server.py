import socket
import threading

HOST = ''
PORT = 20000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

udp.bind((HOST, PORT))

clients = {}    # guarda IP e nome de clientes ativos no momento

def receive(msg, client):

    while True:
        msg = msg.decode().split(":")
        print("msg " + msg)
        if msg[0] == 'USER':
            print("Conectado a cliente " + msg[1])
            clients[client] = msg[1] # adiciona em clientes conectados
        elif msg[0] == 'MSG':
            for client_socket in clients: # para todo cliente ativo
                if client_socket != client: # exceto para o cliente que enviou a msg
                    text = "MSG:" + clients[client] + ":" + msg[1]
                    udp.sendto(text.encode(), client_socket) # envia msg
        elif msg[0] == 'LIST':
            text = "Online:\n"
            for client_socket in clients: # todos os clientes conectados
                text += clients[client_socket] + ", "
            udp.sendto(text.encode, client) # envia apenas para quem pediu a lista
        elif msg[0] == 'BYE':
            print("Encerrando conexão de cliente " + clients[client])
            del clients[client] # remove de clientes conectados
            break

        print(client, msg)
        msg, client = udp.recvform(1024)

    return

print("esperando conexão...")
msg, client = udp.recvfrom(1024)

while True:
    t = threading.Thread(target=receive, args=(msg,client))
    t.start()

udp.close()

# while True:
#     print('esperando...')
#     msg, client = udp.recvfrom(1024)
#     print(client, msg.decode())
#     udp.sendto('ack'.encode(), client)

# tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# tcp.bind((HOST, PORT))

# tcp.listen(1)





