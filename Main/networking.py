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
class Account():
    def __init__(self):
        self.__username = ""   #3 < size < 15
        self.__password = ""   #7 < size

    def enter_Details(self):

        while not len(username) in range(5, 21):
            username = input("Enter Username: ")

        while not len(password) >= 7:
            password = input("Enter Password: ")

        #Convert password into hash

        self.__username = username
        self.__password = hashlib.sha256(password.encode()).hexdigest()


class Client:

    def __init__(self):
        self.__host = "127.0.0.1"
        self.__port = 7777
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        
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
                print("Login success")

        else:
            print("No proceed")

        return valid


    """
    def match_Players(self):
        print("Doing login stuff on client")
        self.__client.sendall(self.request.encode())
        proceed = self.__client.recv(1024).decode()
        if proceed:
            pass
        else:
            return #connection no go
    """
    
    """
    def play_Multiplayer(self):
        print("Doing login stuff on client")
        self.__client.sendall(self.request.encode())
        proceed = self.__client.recv(1024).decode()

        if proceed:
            pass
        else:
            return #connection no go
    """




