import socket
from threading import Thread
import sqlite3

import time

host = "127.0.0.1"
port = 7777

username, password = "heehee", "ohoo"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()

def register(server):
    print("Doing register stuff on server")
    server.sendall("proceed".encode())
    details = server.recv(1024).decode().split(",")

def login(server):
    print("doing login stuff on server")
    server.sendall("proceed".encode())
    details = server.recv(1024).decode().split(",")
    if details[0] == username and details[1] == password:
        print("Deets match")
        pass#if username in database
        #if passwords match
        #send ;ogin valid
        #Add user to online players
        #return
    else:
        print("deets dont match")
        pass
        #try again

def match_Players(server):
    print("Doing login stuff on server")

def play_Multiplayer(server):
    print("Doing login stuff on server")


options = {"login": login,
        "register": register,
        "match_Players": match_Players,
        "play_Multiplayer": play_Multiplayer}


print("Server")

while True:

    client, address = server.accept()

    
    request = client.recv(1024).decode()
    print(request)

    
    if request in options:
        Thread(options[request](client))
    
