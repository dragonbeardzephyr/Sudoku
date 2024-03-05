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
def check(username, cursor):
    res = cursor.execute(f"SELECT Username FROM Accounts WHERE Username = '{username}'")
    if res == username:
        return True
    else:
        return False


def verify(username, password, cursor):#Checks if username an dpassword match
    if check(username, cursor):
        usernameResult = cursor.execute()
        passwordResult = cursor.execute()
        if usernameResult == username and passwordResult == password:
            return True
        else:
            return False
    else:
        return False
  
def register(server):
    print("Doing register stuff on server")
    server.sendall("proceed".encode())
    details = server.recv(1024).decode().split(",")
    conn = sqlite3.connect("")
    cursor = conn.cursor()
    if check(details[0], conn):
        cursor.execute("INSERT")
    
    conn.close()


    
def login(server):
    print("doing login stuff on server")
    server.sendall("proceed".encode())
    details = server.recv(1024).decode().split(",")

    conn = sqlite3.connect("")
    cursor = conn.cursor()

    if verify(details[0], details[1], cursor):
        pass#Login was good
    else:
        pass # Login badd

    conn.close()

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
    
