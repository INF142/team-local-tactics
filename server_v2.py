import numbers
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from threading import *
import team_local_tactics as tlt
from _thread import *
import pickle

threads = []


class Client_thread(Thread):
    def __init__(self,conn,adr, number, champ_list):
        Thread.__init__(self)
        self.csocket = conn
        self.cadr = adr
        self.client_number = str(number)
        self.champ_list = champ_list
        print("client at adress ", adr)
        print("connection at: ", conn)
        
    def run(self):
        print("connection from", self.cadr)
        self.csocket.send(self.client_number.encode())
        self.csocket.send(pickle.dumps(self.champ_list))    

def get_champion_from_client(connection, num):
        #if num == lock:
        print(connection.recv(1024).decode())
        print(connection.recv(1024).decode())
            #num = num + 1
        #else:
            #get_champion_from_client(connection, num)


def main():
    threadCount = 0
    sock = socket()
    csock = socket()
    csock.connect(('localhost', 8888))
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(("localhost", 5555))
    print('The server is ready to receive')

    champ_list = pickle.loads(csock.recv(1024))

    while True:
        sock.listen()
        conn, adr = sock.accept()
        threadCount = threadCount + 1
        newthread = Client_thread(conn, adr, threadCount, champ_list)
        newthread.start()
        #conn.send('1'.encode())
        #conn.send(pickle.dumps(champ_list))
        #conn.close()
        

    
if __name__ == "__main__":
    main()
    
#TODO: implement threading