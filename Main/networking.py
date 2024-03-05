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


username, password = "heehee", "boohoo"
class Client:

    def __init__(self):
        self.__host = "127.0.0.1"
        self.__port = 7777
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.account = Account()
        self.request = ""

        self.options = {"login": self.login,
        "register": self.register,
        "match_Players": self.match_Players,
        "play_Multiplayer": self.play_Multiplayer}


    def handle(self, request):
        self.request = request
        if request in self.options:
            self.__client.sendall(self.request.encode())
            self.options[request]
        else:
            print("Inavlid request")

    def connect(self):
        try:
            self.__client.connect((self.__host, self.__port))
        except:
            print("Connection could not be made")


    def register(self):
        print("Doing register stuff on client")

        proceed = self.__client.recv(1024).decode()

        if proceed == "proceed":
            self.account.enter_Details()
            self.__client.send((username+","+password).encode())

            if self.__client.recv(1024).decode() == "valid":
                    valid = True

                    

        else:
            print("No proceed")
            return #connection no go
    


    def login(self):
        print("doing login stuff on client")

        self.__client.sendall(self.request.encode())

        proceed = self.__client.recv(1024).decode()


        if proceed == "proceed":
            valid = False
            while valid == False:
                self.account.enter_Details()

                self.__client.send((username+","+password).encode())

                if self.__client.recv(1024).decode() == "valid":
                    valid = True

                

        else:
            print("No proceed")
            return #connection no go



    def match_Players(self):
        print("Doing login stuff on client")
        self.__client.sendall(self.request.encode())
        proceed = self.__client.recv(1024).decode()
        if proceed:
            pass
        else:
            return #connection no go


    def play_Multiplayer(self):
        print("Doing login stuff on client")
        self.__client.sendall(self.request.encode())
        proceed = self.__client.recv(1024).decode()

        if proceed:
            pass
        else:
            return #connection no go






