from socket import socket
from rich import print
from rich.prompt import Prompt

player_number = 0
sock = socket()

def set_player_number(player_n):
    #print(player_n)
    player_number = player_n
    #print(player_number)

def connect(address, port):    
    server_adress = (address, port)
    sock.connect(server_adress)     
    
       
def main():
    connect("localhost", 5555)
    print(sock.recv(1024).decode())
    set_player_number(sock.recv(1024).decode)
    sock.close()

if __name__ == "__main__":
    main()