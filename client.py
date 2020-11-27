# Manoela Werneck 95664
# Matheus Ximenes 95666

import socket
import threading

HOST = '127.0.0.1'
PORT = 20000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv = (HOST, PORT)

connected = True # bool de controle

def receiveFile(con, name):
    data = con.recv(1024)
    if (data):
        f = open('./clientFiles/' + name,'wb') # arquivos do cliente em pasta diferente para testar transferência
        while 1:
            f.write(data)
            data = con.recv(1024)
            if not data:
                break
        f.close()

    return

def sendFile(con, name):
    f = open('./clientFiles/' + name,'rb') # arquivos do cliente em pasta diferente para testar transferência
    for msg in f.readlines():
        con.send(msg)
    f.close()

    return

# funcao que mapeia o comando nas palavras-chave do protocolo
def send():
    while True:
        msg = input().split(" ")

        # solicitar lista de clientes ativos
        if msg[0] == '/list':
            text = "LIST"
            udp.sendto(text.encode(), serv)

        # enviar arquivo
        elif msg[0] == '/file':
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect(serv)
            text = "FILE:" + msg[1]
            udp.sendto(text.encode(), serv)
            sendFile(tcp, msg[1])
            tcp.close()

        # baixar arquivo
        elif msg[0] == '/get':
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect(serv)
            text = "GET:" + msg[1]
            udp.sendto(text.encode(), serv)
            receiveFile(tcp, msg[1])
            tcp.close()

        # desconectar
        elif msg[0] == '/bye':
            text = "BYE"
            udp.sendto(text.encode(), serv)
            connected = False
            break

        # enviar msg de texto
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
            if msg[1] == 'disconnect': # se for desconectado para de ouvir o servidor
                break             
            elif len(msg) < 3:
                print(msg[1])
            else:
                print(msg[1] + ': ' + msg[2])
        elif msg[0] == 'MSG':
            print(msg[1] + ': ' + msg[2])

    return

msg = input('Nome de usuário: ') # exige nome antes de conectar cliente
text = "USER:" + msg
udp.sendto(text.encode(), serv)

t1 = threading.Thread(target=send, args=())
t1.start()

t2 = threading.Thread(target=listen, args=())
t2.start()