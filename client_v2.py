from socket import socket
from rich import print
from rich.prompt import Prompt
from rich.table import Table
import pickle

sock = socket()

def get_player_number() -> int:
    player = sock.recv(1024).decode()
    print(type(player))
    print(player)
    return int(player)
 

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
    player = get_player_number()
    print('\n'
          'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
          '\n'
          'You are now connectet to our server!\n'
          'When there is two players connected, you will get the opportunity to pick your first champion. \n'
          '\n\nYou are player number {0} \n'.format(player))
    
    
    print(print_available_champs(pickle.loads(sock.recv(1024))))
    sock.send("rello".encode())
    
    for _ in range (2):
        print(sock.recv(1024).decode())
        sock.send(input(">").encode())
        print(sock.recv(1024).decode())
    
    #print(sock.recv(1024).decode())

    sock.close()

if __name__ == "__main__":
    main()