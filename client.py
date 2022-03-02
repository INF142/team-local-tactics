from socket import socket
from rich import print
from rich.prompt import Prompt
import pickle
import team_local_tactics as tlt

sock = socket()


def connect(address, port):    
    server_adress = (address, port)
    sock.connect(server_adress)     
    
       
def main():
    connect("localhost", 5555)
    print(sock.recv(1024).decode())
    tlt.print_available_champs(pickle.loads(sock.recv(1024)))
    input("> ")
    sock.close()

if __name__ == "__main__":
    main()