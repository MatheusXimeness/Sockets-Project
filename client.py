import socket
import threading

HOST = '127.0.0.1'
PORT = 20000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv = (HOST, PORT)
udp.bind(serv)

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
            break
        else:
            text = "MSG:" + " ".join(msg)

        udp.sendto(text.encode(), serv)

    return;

msg = input('Nome de usuário: ')
text = "USER:" + msg
udp.sendto(text.encode(), serv)

t = threading.Thread(target=send, args=())
t.start()

udp.close()

# while msg != '/bye':
#     udp.sendto(msg.encode(), (HOST, PORT))
#     msg, serv = udp.recvfrom(1024)
#     print(serv, msg.decode())
#     msg = input()

