from email import message
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
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.username = ""
        """
        self.options = {"login": self.login,
        "register": self.register,
        "match_Players": self.match_Players,
        "play_Multiplayer": self.play_Multiplayer}
        """

    """
    def handle(self, request):
        if request in self.options:
            self.__client.sendall(request.encode())
            self.options[request]
        else:
            print("Inavlid request")
    """
    def connect(self):
        try:
            self.__client.connect((self.__host, self.__port))
            self.connected = True
        except :
            print("Connection could not be made")
            return False

    def disconnect(self):
        self.__client.close()
        self.connected  = False

    def send(self, message):
        self.__client.send(message.encode())

    def receive(self):
        return self.__client.recv(1024).decode()
    
    def hashPW(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):#Password going through here is here unproccessed
        print("Doing register stuff on client")

        self.__client.sendall("register".encode())
        proceed = self.__client.recv(1024).decode()

        valid = False

        if proceed == "proceed":
            self.__client.send((username+","+self.hashPW(password)).encode())
            if self.__client.recv(1024).decode() == "valid":
                    valid = True

                    

        else:
            print("No proceed")

        return valid
    


    def login(self, username, password, hashed):
        print("doing login stuff on client")
        
        self.__client.sendall("login".encode())

        proceed = self.__client.recv(1024).decode()

        valid = False

        if proceed == "proceed":
            if hashed is True:
                self.__client.send((username+","+password).encode())
            else:
                self.__client.send((username+","+self.hashPW(password)).encode())

            if self.__client.recv(1024).decode() == "valid":
                valid = True
                self.username = username
                print("Login success")

        else:
            print("No proceed")

        return valid

    def update_BestTimes(self, times):
        print("Doing update best times stuff on client")
        self.__client.sendall("update_BestTimes".encode())
        proceed = self.__client.recv(1024).decode()
        if proceed == "proceed":
            self.__client.send((f"{self.username}," + ",".join(times)).encode())
        else:
            return

    def match_Players(self, difficulty):
        print("Doing login stuff on client")
        self.__client.sendall("match_Players".encode())
        proceed = self.__client.recv(1024).decode()
        if proceed == "proceed":
            self.__client.send(difficulty.encode())
            message = self.__client.recv(1024).decode()
            if message == "Enqueued":
                return True
            elif message == "Queue full":
                return False
        else:
            return #connection no go
    
    
    """
    def play_Multiplayer(self):
        print("Doing login stuff on client")
        self.__client.sendall("play_Multiplayer".encode())
        proceed = self.__client.recv(1024).decode()

        if proceed:
            pass
        else:
            return #connection no go
    """




