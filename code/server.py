import socket
import threading
import pickle
import struct

HEADER = 64
PORT = 2048
SERVER = socket.gethostname()
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
HOSTS = False
HAS = False
SHUFFLE = []
DICO = {}


def hashs(data, nb_computers):
    data = data.split(" ")
    if data[-1] == "":
        data.pop()
    if data[0] == "":
        data.pop(0)
    l = [[] for i in range(nb_computers)]
    for value in data:
        ord3 = lambda x: '%.3d' % ord(x)
        hash_value = int(''.join(map(ord3, value))) % nb_computers
        l[hash_value].append(value)
    return l


def wordcount(text):
    dico = {}
    for mot in text:
        if mot not in dico:
            dico[mot] = 1
        else:
            dico[mot] += 1
    return dico


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


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = recv_msg(conn).decode(FORMAT)
        print(f'[{SERVER}] received {msg} from [{addr[0]}]')
        if msg == DISCONNECT_MESSAGE:
            connected = False
        elif msg == 'HOSTS':
            global HOSTS
            HOSTS = pickle.loads(recv_msg(conn))
            print(f'[{SERVER}] received {HOSTS} from [{addr[0]}]')
        elif msg == 'SHUFFLE':
            global SHUFFLE
            SHUFFLE.append(pickle.loads(recv_msg(conn)))
            print(f"[{SERVER}] received {len(SHUFFLE[-1])} from [{addr[0]}]")
        elif msg == 'SPLIT':
            msg = recv_msg(conn).decode(FORMAT)
            print(f"[{SERVER}] received {len(msg)} from [{addr[0]}]")
            global HAS
            HAS = hashs(msg, len(HOSTS))
            print(f'[{SERVER}]: finish SPLIT!')
            event_end_split.set()
            event_end_shuffle.wait()
            print(f'[{SERVER}], size: {len(pickle.dumps(DICO))}')
            send_msg(conn, pickle.dumps(DICO))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENNING] Server is listenning on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def shuffle():
    for i in range(len(HOSTS)):
        if HOSTS[i] != SERVER:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                addr = (HOSTS[i], PORT)
                s.connect(addr)
                send_msg(s, "SHUFFLE".encode(FORMAT))
                send_msg(s, pickle.dumps(HAS[i]))
                send_msg(s, DISCONNECT_MESSAGE.encode(FORMAT))
        else:
            global SHUFFLE
            SHUFFLE.append(HAS[i])

    while True:
        if len(SHUFFLE) == len(HOSTS):
            break
    print(f'[{SERVER}]: finish SHUFFLE!')
    global DICO
    DICO = wordcount(sum(SHUFFLE, []))
    event_end_shuffle.set()


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    print('[Starting] the server ...')

    event_end_split = threading.Event()
    event_end_shuffle = threading.Event()

    thread = threading.Thread(target=start)
    thread.start()

    event_end_split.wait()

    thread = threading.Thread(target=shuffle)
    thread.start()
