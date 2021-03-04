import socket
import pickle
from pieces import generatePieces
from generate import Generator
from player import Player
from _thread import *
import sys

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



try:
    s.bind((server, port))

except socket.error as e:
    str(e)



s.listen(2)
print("Waiting for another player to connect")


grid = Generator.generateGrid()
p1Pieces = generatePieces("player1", grid)
p2Pieces = generatePieces("player2", grid)
players = [Player(p1Pieces, grid), Player(p2Pieces, grid)]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("A player has disconnected")
                break

            else:
                if player == 1:
                    reply = players[0]

                else:
                    reply = players[1]



            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("Disconnected")
    conn.close()


currentPlayers = 0
while True:
    conn, addr = s.accept()
    print(addr, "has connected")

    start_new_thread(threaded_client, (conn, currentPlayers))
    currentPlayers += 1
