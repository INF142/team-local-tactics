from socket import socket, SOL_SOCKET, SO_REUSEADDR
import pickle
import team_local_tactics as tlt

sock = socket()
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind(("localhost", 8888))
sock.listen()

while True:
        conn, _ = sock.accept()
        conn.send(pickle.dumps(tlt.load_some_champs()))
        conn.close()
        
#TODO: implement a datbase