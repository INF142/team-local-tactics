from socket import socket, SOL_SOCKET, SO_REUSEADDR
from threading import *
import threading
import team_local_tactics as tlt
from _thread import *
import pickle

threads = []
champions_selected = []
mylock = threading.Lock()
player1 = []
player2 = []
champ_list = {}

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
        counter = 1

        print("number is: ", self.client_number)
        self.csocket.send(self.client_number.encode())
        self.csocket.send(pickle.dumps(self.champ_list))
        print(self.csocket.recv(1024))
        for _ in range(2):
            if int(self.client_number)==counter:
                counter = counter + 1
                mylock.acquire()
                input_champion(self.csocket, self.champ_list, player1, player2)
                mylock.release()
                continue
            else:
                counter = counter - 1 
                mylock.acquire()
                input_champion(self.csocket, self.champ_list, player2, player1)
                mylock.release()
                continue
        
        
def input_champion(connection: socket,
                   champions,
                   p1: list[str],
                   p2: list[str]) -> None:

    #Prompt the player to choose a champion and provide the reason why
    #certain champion cannot be selected
    
    print(f"talking to {connection}")
    while True:
        print("in the while loop")
        connection.send(("Please input a Champion!").encode())
        name = connection.recv(1024).decode()
        print (name)
        match name:
            case name if name not in champions:
                connection.send((f"The champion {name} is not available. Try again.").encode())
            case name if name in p1:
                connection.send((f'{name} is already in your team. Try again.').encode())
            case name if name in p2:
                connection.send((f'{name} is in the enemy team. Try again.').encode())
            case _:
                p1.append(name)
                connection.send((f"{name} is added to your rooster.").encode())
                print(p1)
                break
        

def main():
    threadCount = 0
    sock = socket()
    csock = socket() #connects to game data server
    csock.connect(('localhost', 8888))
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(("localhost", 5555))
    print('The server is ready to receive')

    champ_list = pickle.loads(csock.recv(1024))

    while True:
        sock.listen()
        conn, adr = sock.accept()
        threadCount = threadCount + 1
        #newthread = Client_thread(conn, adr, threadCount, champ_list)
        
        threads.append(Client_thread(conn, adr, threadCount, champ_list))
        #print(mylock)
        if len(threads) == 2:
            for t in threads:
                print("connection at: ", t.csocket)
                t.start()

            #for _ in range(2):
                #input_champion(threads[0].csocket, champ_list, player1, player2)
                #input_champion(threads[1].csocket, champ_list, player1, player2)
        #sock.close()
        #newthread.start()

                
    
        

    
if __name__ == "__main__":
    main()
    
#TODO: implement threading