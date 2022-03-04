import numbers
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from threading import *
import threading
import team_local_tactics as tlt
from _thread import *
import pickle

threads = []
champions_selected = []
mylock = 2

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
        print("number is: ", self.client_number)
        self.csocket.send(self.client_number.encode())
        self.csocket.send(pickle.dumps(self.champ_list))
        #if mylock != int(self.client_number):
        #    threading.Lock().acquire()
        #    print(f"thread {self.client_number} should have the lock")
        self.csocket.send("give me a champ, champ!".encode())
        #for i in range(2):
        #    self.csocket.send(pickle.dumps(champions_selected))
        #    print(self.csocket.recv(1024).decode())
        self.csocket.close()
        

#def get_champion_from_client(connection, num):
 #       glock = threading.Lock()
  #      undefined


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
        #threads.append(newthread)
        #print(threads)
        newthread.start()
        

    
if __name__ == "__main__":
    main()
    
#TODO: implement threading