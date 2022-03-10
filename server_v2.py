from socket import socket, SOL_SOCKET, SO_REUSEADDR
from threading import *
import threading
import team_local_tactics as tlt
from _thread import *
import pickle
from core import  Match, Shape, Team, Champion
from rich.table import Table

threads = []
champions_selected = []
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
        print(self.csocket.recv(1024))
        if self.client_number == "1":
            me = player1
            other = player2
        else:
            me = player2
            other = player1
        for _ in range (2):
            input_champion(self.csocket, self.champ_list, me, other)
            
        
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
            
def print_match_summary(match: Match) -> None:
    
    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red",
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column("Blue",
                                 style="blue",
                                 no_wrap=True)

        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        print(round_summary)
        print('\n')

    # Print the score
    red_score, blue_score = match.score
    print(f'Red: {red_score}\n'
          f'Blue: {blue_score}')

    # Print the winner
    if red_score > blue_score:
        print('\n[red]Red victory! :grin:')
    elif red_score < blue_score:
        print('\n[blue]Blue victory! :grin:')
    else:
        print('\nDraw :expressionless:')
        

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
            for t in threads:
                t.join()

            match = Match(
                Team([champ_list[name] for name in player1]),
                Team([champ_list[name] for name in player2])
            )
            match.play()
            tlt.print_match_summary(match)
        

                
    
        

    
if __name__ == "__main__":
    main()
    
#TODO: implement threading