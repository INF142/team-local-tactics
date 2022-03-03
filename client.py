from socket import socket
from rich import print
from rich.prompt import Prompt
from rich.table import Table
import pickle

sock = socket()
    

def connect(address, port):    
    server_adress = (address, port)
    sock.connect(server_adress)     
    
def print_available_champs(champions):
        # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    # Populate the table
    for champion in champions.values():
        available_champs.add_row(*champion.str_tuple)
    
    return available_champs
    
       
def main():
    connect("localhost", 5555)
    print(sock.recv(1024).decode())
    
    champions = pickle.loads(sock.recv(1024))
    
    sock.send((">>").encode())
    
    choose_champ_message = sock.recv(1024).decode()
    
    
    print(choose_champ_message)
    
    #print(champions)
    
    print(choose_champ_message)
    print(print_available_champs(champions))
    
    a = input("> ")

    sock.close()

if __name__ == "__main__":
    main()