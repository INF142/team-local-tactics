from socket import socket, SOL_SOCKET, SO_REUSEADDR
from threading import *
import threading
import team_local_tactics as tlt
from _thread import *
import pickle

threads = []
champions_selected = []
mylock = 1
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
        print("number is: ", self.client_number)
        self.csocket.send(self.client_number.encode())
        self.csocket.send(pickle.dumps(self.champ_list))
        
        #self.csocket.send(("This is where we fail folks!").encode())

        #self.csocket.close()
        
def input_champion(connection: socket,
                   champions,
                   player1: list[str],
                   player2: list[str]) -> None:

    #Prompt the player to choose a champion and provide the reason why
    #certain champion cannot be selected
    
    while True:
        connection.send(("Please input a Champion!").encode())
        name = connection.recv(1024).decode()
        print (name)
        match name:
            case name if name not in champions:
                connection.send((f"The champion {name} is not available. Try again.").encode())
            case name if name in player1:
                connection.send((f'{name} is already in your team. Try again.').encode())
            case name if name in player2:
                connection.send((f'{name} is in the enemy team. Try again.').encode())
            case _:
                player1.append(name)
                connection.send((f"{name} is added to your rooster."))
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
        if len(threads) == 2:
            for t in threads:
                print("connection at: ", t.csocket)
                t.start()
            for _ in range(2):
                input_champion(threads[0].csocket, champ_list, player1, player2)
                input_champion(threads[1].csocket, champ_list, player1, player2)
                
    
        

    
if __name__ == "__main__":
    main()
    
#TODO: implement threading