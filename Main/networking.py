
import socket
import hashlib

#Make connection with server
#Select if you want to play against a random
#get added to queue of players
#get put into a lobby
#play against player win lose
#continue 
#if dont continue exit mulitplayer
#close connection

class Client:
    def __init__(self):
        self.__host = "127.0.0.1"
        self.__port = 7777
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP connection
        self.connected = False
        self.username = ""

    def connect(self):
        try:
            self.__client.connect((self.__host, self.__port))
            self.connected = True
            print("[Connection with server established]")
        except:
            print("[Connection could not be made]")
            return False

    def disconnect(self):
        self.__client.send("Logout".encode())
        self.__client.close()
        self.connected  = False

    def send(self, message):
        self.__client.send(message.encode())

    def receive(self, n = 1024):# n = bytes to receive
        return self.__client.recv(n).decode()
    
    def hash_Password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):#Password going through here is here unproccessed
        self.__client.send("register".encode())
        proceed = self.__client.recv(1024).decode()

        valid = False

        if proceed == "proceed":
            self.__client.send((username+","+self.hash_Password(password)).encode())
            if self.__client.recv(1024).decode() == "valid":
                    valid = True

        else:
            print("No proceed")

        return valid
    


    def login(self, username, password, hashed : bool):
        print("[Login from client]")
        
        self.__client.send("login".encode())

        proceed = self.__client.recv(1024).decode()
        print(proceed)
        valid = False

        if proceed == "proceed":
            if hashed is True:
                self.__client.send((username+","+password).encode())
            else:
                self.__client.send((username+","+hash_Password(password)).encode())

            if self.__client.recv(1024).decode() == "valid":
                valid = True
                self.username = username
                print("Login success")

        else:
            print("No proceed")

        return valid


    def update_BestTimes(self, times):
        self.__client.send("update_BestTimes".encode())
        
        proceed = self.__client.recv(1024).decode()
        
        if proceed == "proceed":
            self.__client.send((f"{self.username}," + ",".join(times)).encode())
            if self.__client.recv(1024).decode() == "valid":
                return True
            else:
                return False


    def match_Players(self, difficulty): 
        self.__client.send("match_Players".encode())
        
        proceed = self.__client.recv(1024).decode()

        if proceed == "proceed":
            print("proceed = true sending difficulty")
            self.__client.send(difficulty.encode())
            message = self.__client.recv(1024).decode()
            print(message)
            if message == "Enqueued":
                return True
            elif message == "Queue full":
                return False
        else:
            return #connection no go
        
    
    """
    def play_Multiplayer(self):
        print("Doing login stuff on client")
        self.__client.send("play_Multiplayer".encode())
        proceed = self.__client.recv(1024).decode()

        if proceed:
            pass
        else:
            return #connection no go
    """




