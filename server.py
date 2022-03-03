from socket import socket, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
import team_local_tactics as tlt
from _thread import *
import pickle

threads = []
lock = 1

def get_champion_from_client(connection, num):
        #if num == lock:
        print(connection.recv(1024).decode())
        print(connection.recv(1024).decode())
            #num = num + 1
        #else:
            #get_champion_from_client(connection, num)

def multi_threaded_client(connection, thread_num):
    connection.send('\n'
          'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
          '\n'
          'Each player choose a champion each time.'
          '\n\nYou are player number {0} \n'.format(thread_num).encode())
    connection.send(pickle.dumps(tlt.load_some_champs()))
    get_champion_from_client(connection, thread_num)
    connection.send("this is the server".encode())

def main():
    sock = socket()
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(("localhost", 5555))
    sock.listen()
    print('The server is ready to receive')
    threadcount = 0
    while True:
        conn, _ = sock.accept()
        threadcount = threadcount + 1
        threads.append(start_new_thread(multi_threaded_client, (conn, threadcount)))
                

    
if __name__ == "__main__":
    main()
