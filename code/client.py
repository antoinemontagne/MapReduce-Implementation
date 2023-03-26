import socket
import threading
import time
import pickle
import struct
import os

PATH = '\\'.join(os.getcwd().split('\\')[:-1])
NOM_FICHIER = 'split_final.txt'
SERVER = socket.gethostname()
PORT = 2048
FORMAT = 'utf-8'
#ces noms de machines doivent être les mêmes que ceux spécifiés dans le deploy.sh
HOSTS = ["nom_machine1", "nom_machine2", "nom_machine3"]
DISCONNECT_MESSAGE = '!DISCONNECT'
FINAL_RESULT = []


def concat_dicos(dicos):
    Fdico = {}
    for d in dicos:
        Fdico.update(d)
    return Fdico


def send_msg(sock, msg):
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recvall(sock, msglen)


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def client_program():
    with open(PATH + '/data/' + NOM_FICHIER, "rb") as f:
        text = f.read().decode(FORMAT)
        read_size = int(len(text) / len(HOSTS))
        file_read = 0
        for computer in HOSTS:
            if computer == HOSTS[len(HOSTS) - 1]:
                bytes_read = text[file_read:]
            else:
                bytes_read = text[file_read:file_read + read_size]
                file_read += read_size
                if bytes_read[-1] != ' ':
                    for i in range(1, len(bytes_read)):
                        if bytes_read[len(bytes_read) - (i + 1):len(bytes_read) - i] == ' ':
                            bytes_read = bytes_read[:len(bytes_read) - i]
                            file_read -= i
                            break
            print(f'To [{computer}], split size: {len(bytes_read)} bytes')
            thread = threading.Thread(target=handle_client, args=(computer, bytes_read.encode(FORMAT)))
            thread.start()


#gestion de la connexion à un serveur sur les machines contenues dans HOSTS
def handle_client(computer, bytes_read):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        addr = (computer, PORT)
        s.connect(addr)
        print(f"Connexion to [{addr[0]}]")
        send_msg(s, "HOSTS".encode(FORMAT))
        send_msg(s, pickle.dumps(HOSTS))
        send_msg(s, "SPLIT".encode(FORMAT))
        send_msg(s, bytes_read)
        global FINAL_RESULT
        FINAL_RESULT.append(pickle.loads(recv_msg(s)))
        print(f'from [{computer}], size received: {len(FINAL_RESULT[-1])}')
        send_msg(s, DISCONNECT_MESSAGE.encode(FORMAT))


if __name__ == '__main__':
    begin = time.time()

    print("Démarrage")
    client_program()

    while True:
        if len(FINAL_RESULT) == len(HOSTS):
            break

    FINAL_RESULT = concat_dicos(FINAL_RESULT)
    value_key_pairs = ((value, key) for (key, value) in FINAL_RESULT.items())
    sorted_value_key_pairs = sorted(value_key_pairs, reverse=True)
    FINAL_RESULT = {k: v for v, k in sorted_value_key_pairs}
    with open(PATH + '/data/result.txt', "w") as fichier:
        fichier.write(str(FINAL_RESULT))

    print(f'The program executed in {time.time() - begin}')