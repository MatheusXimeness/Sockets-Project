import socket
import threading

HOST = '127.0.0.1'
PORT = 20000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv = (HOST, PORT)
# udp.bind(serv)

connected = True # bool de controle

# funcao que codifica o comando nas palavras-chave do protocolo
def send():

    while True:
        msg = input().split(" ")
        if msg[0] == '/list':
            text = "LIST"
        elif msg[0] == '/file':
            text = "FILE:" + msg[1]
            # criar conexao TCP...
        elif msg[0] == '/get':
            text = "GET:" + msg[1]
            # criar conexao TCP...
        elif msg[0] == '/bye':
            text = "BYE"
            udp.sendto(text.encode(), serv)
            connected = False
            break
        else:
            text = "MSG:" + " ".join(msg)

        udp.sendto(text.encode(), serv)

    udp.close()
    return

def listen():
    while connected:
        msg, client = udp.recvfrom(1024)
        msg = msg.decode().split(":")
        if msg[0] == 'INFO':
            print(msg[1])
        elif msg[0] == 'MSG':
            print(msg[1] + ': ' + msg[2])

    return

msg = input('Nome de usuário: ')
text = "USER:" + msg
udp.sendto(text.encode(), serv)

t1 = threading.Thread(target=send, args=())
t1.start()

t2 = threading.Thread(target=listen, args=())
t2.start()

# while msg != '/bye':
#     udp.sendto(msg.encode(), (HOST, PORT))
#     msg, serv = udp.recvfrom(1024)
#     print(serv, msg.decode())
#     msg = input()
