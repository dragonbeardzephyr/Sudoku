import socket
#import hashlib

#Make connection with server
#Select if you want to play against a random
#get added to queue of players
#get put into a lobby
#play against player win lose
#continue
#if dont continue exit mulitplayer
#close connection

def gaviHash(data):
    hash_value = 0
    x = len(data)
    for i, char in enumerate(data):
        # Mix operations: XOR, multiplication, bit-shifting
        hash_value ^= (ord(char) * (x**i))
        hash_value ^= (ord(char) << ((x-i) % 3)) ** ((x-i))
        
    return hex(hash_value)[2:]


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
        print("[Connection with server closed]")

    def send(self, message):
        self.__client.send(message.encode())

    def receive(self, n = 1024):# n = bytes to receive
        return self.__client.recv(n).decode()

    def hash_Password(self, password):
        return gaviHash(password)

    def register(self, username, password):#Password going through here is here unproccessed
        print("[Registering from client]")
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

        valid = False

        if proceed == "proceed":
            if hashed is True:
                self.__client.send((username+","+password).encode())
            else:
                self.__client.send((username+","+self.hash_Password(password)).encode())

            if self.__client.recv(1024).decode() == "valid":
                valid = True
                self.username = username
                print("Login success")

        return valid


    def update_BestTimes(self, times):
        print("[Updating best times from client]")

        self.__client.send("update_BestTimes".encode())
        proceed = self.__client.recv(1024).decode()

        if proceed == "proceed":
            self.__client.send((f"{self.username}," + ",".join(times)).encode())
            if self.__client.recv(1024).decode() == "valid":
                return True
            else:
                return False


    def match_Players(self, difficulty):
        print("[Entering player for matchmaking from client]")
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





    
    
    
if __name__ == "__main__":
    while True:
        print(gaviHash(input(">")))