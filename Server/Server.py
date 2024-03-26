import socket
from threading import Thread
import sqlite3

import time

host = "127.0.0.1"
port = 7777

DATABASE = "Server\Sudoku_Online.db"





def check(username, cursor):
    result = cursor.execute("SELECT Username FROM Accounts WHERE Username = ?", (username,)).fetchone()
    print(f"result: {result}")   
    if result is None:
        print("username not in database")
        return False
    elif username in result:
        print("username in database")
        return True
    
        


def verify(username, password, cursor):#Checks if username an dpassword match
    if check(username, cursor):
        print(username, password)
        result = cursor.execute("SELECT Username, Password FROM Accounts WHERE Username = ? AND Password = ?", (username, password)).fetchone()
        print(result)
        if result is None:
            print("Result none")
            return False
            
        else:
            usernameResult, passwordResult = result
            print(username, password)
            print(usernameResult, passwordResult)
            if usernameResult == username and passwordResult == password:
                return True
            else:
                return False
    else:
        return False


def register(client):
    print("Doing register stuff on client")
    client.sendall("proceed".encode())
    details = client.recv(1024).decode().split(",")
    print(details)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if check(details[0], cursor):
        client.sendall("invalid".encode())#USername already exists
        conn.close()
        return False
    
    else:
        cursor.execute("INSERT INTO Accounts (Username, Password) VALUES (?, ?)", (details)) # Tuple unpacking if not obvious
        cursor.execute("INSERT INTO BestTimes (Username, Easy, Normal, Hard, 'Extra Hard') VALUES (?, NULL, NULL, NULL, NULL)", (details[0],)) # Tuple unpacking if not obvious

        client.sendall("valid".encode())
        conn.commit()
        conn.close()
        print("INserted")
        return True
    
def login(client):
    print("doing login stuff on sever")
    client.sendall("proceed".encode())
    details = client.recv(1024).decode().split(",")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if verify(details[0], details[1], cursor):
        print(f"Login good by {details[0]}")
        client.sendall("valid".encode())
        conn.close()
        return True
    else:
        client.sendall("invalid".encode())
        print("Login bad")# Login badd
        conn.close()
        return False

def update_BestTimes(client):
    client.sendall("proceed".encode())
    times = client.recv(1024).decode().split(",")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE BestTimes SET Easy = ?, Normal = ?, Hard = ?, 'Extra Hard' = ? WHERE Username = ?", (times[1], times[2], times[3], times[4], times[0]))
        client.sendall("valid".encode())
        
    except Exception as e:
        print(f"Error updating best times {e}")
        client.sendall("invalid".encode())

    conn.commit()
    conn.close()
    


def match_Players(client):
    print("Doing login stuff on client")
    client.sendall("proceed".encode())
    difficulty = client.recv(1024).decode()

def play_Multiplayer(client):
    print("Doing login stuff on client")



options = {"login": login,
        "register": register,
        "match_Players": match_Players,
        "play_Multiplayer": play_Multiplayer,
        "update_BestTimes" : update_BestTimes}


def handle(client, address):
    
    while True:
        try:
            request = client.recv(1024).decode()
            print(request)
            if not request:
                print("not request")
                break
            if request == "Logout":
                print("Logoutheehehe")
                break

            elif request in options:
                options[request](client)
                
        except Exception as e :
            print(f"Inavlid request {e}")
            break

    print("Closing connection")
    client.close()



def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    """
    easyQueue
    normalQueue
    hardQueue
    extraHardQueue
    """

    while True:

        client, address = server.accept()
        print(f"Connection from {address}")

        thread = Thread(target = handle, args = (client, address))
        thread.start()

        print("pong")
        

main()

