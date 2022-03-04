from socket import socket, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
import team_local_tactics as tlt
from _thread import *
import pickle

threads = []

def get_champion_from_client(connection, num):
        #if num == lock:
        print(connection.recv(1024).decode())
        print(connection.recv(1024).decode())
            #num = num + 1
        #else:
            #get_champion_from_client(connection, num)


def main():
    sock = socket()
    csock = socket()
    csock.connect(('localhost', 8888))
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(("localhost", 5555))
    sock.listen()
    print('The server is ready to receive')

    champ_list = pickle.loads(csock.recv(1024))
    print(champ_list)

    while True:
        conn, adr = sock.accept()
        conn.send('1'.encode())
        conn.send(pickle.dumps(champ_list))
        conn.close()
        

    
if __name__ == "__main__":
    main()