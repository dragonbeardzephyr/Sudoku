import socket
import threading
import sqlite3
import random
import time
from Generator.Generate import Puzzle


class Queue():
    def __init__(self, maxSize=10):
        self.__queue = [None for i in range(maxSize)]
        self.__front = 0
        self.__rear = -1
        self.__size = 0
        self.__maxSize = maxSize
        self.lock = threading.Lock()

    def isFull(self):
        return self.__size == self.__maxSize

    def isEmpty(self):
        return self.__size == 0

    def isEven(self):
        #with self.lock:
        return self.__size % 2 == 0

    def enQueue(self, item):
        #with self.lock:
        if self.isFull():
            return item
        else:
            self.__rear = (self.__rear + 1) % self.__maxSize
            self.__queue[self.__rear] = item
            self.__size += 1
            return True
        #print(self.__front, self.__rear)

    def deQueue(self):
        #with self.lock:
        if self.isEmpty():
            return False
        else:
            data = self.__queue[self.__front]
            self.__front = (self.__front + 1) % self.__maxSize
            self.__size -= 1
            return data
        #print(self.__front, self.__rear)

    def show(self):
        return [self.__queue[(self.__front + i) % self.__maxSize]for i in range(self.__size)]

######################################################################

class Client(threading.Thread):
    def __init__(self, client, address):
        super().__init__()
        self.client = client
        self.address = address
        self.username = None
        self.bestTimes = [None, None, None, None]
        self.options = { "login": self.login,
                    "register": self.register,
                    "match_Players": self.match_Players,
                    "update_BestTimes" : self.update_BestTimes}

        self.difficulty = None
        self.matching = False
        self.startMatchingTime = 0
        self.inGame = False

    def run(self):
        while self.client:
            try:
                if self.inGame:
                    continue

                elif self.matching == True:
                    if time.time() - self.startMatchingTime > 300:#After 5 minutes removes player from match queue
                        self.matching = False
                        self.client.send("Match Not Found".encode())
                        print(f"[Matchmaking timed out for {self.username} from {self.address}]")

                else:
                    print(f"[Waiting for request from {self.username}, {self.address}]")

                    request = self.client.recv(1024).decode()
                    print(f"[Request accepted: {request}]")

                    if request == "Logout":
                        print(f"[Logged out has {self.username} from {self.address}]")
                        break

                    elif request in self.options:
                        self.options[request]()

            except Exception as e :
                print(f"[Inavlid request {e}]")
                break


        print(f"[Closing connection {self.username} from {self.address}]")
        self.client.close()

    def check(self, username, cursor):
        result = cursor.execute("SELECT Username FROM Accounts WHERE Username = ?", (username,)).fetchone()
        if result is None:
            return False
        elif username in result:
            return True


    def verify(self, username, password, cursor):#Checks if username an dpassword match
        if self.check(username, cursor):
            result = cursor.execute("SELECT Username, Password FROM Accounts WHERE Username = ? AND Password = ?", (username, password)).fetchone()
            if result is None:
                return False
            else:
                usernameResult, passwordResult = result
                if usernameResult == username and passwordResult == password:
                    return True
                else:
                    return False
        else:
            return False


    #######################################################################
    #Request Redirections
    #######################################################################
    def register(self):
        print(f"[Register request from {self.address}]")
        self.client.send("proceed".encode())
        details = self.client.recv(1024).decode().split(",")
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()

        if self.check(details[0], cursor):
            self.client.send("invalid".encode())#USername already exists
            conn.close()
            print(f"[Account not created, username already taken from {self.address}]")
            return False

        else:
            cursor.execute("INSERT INTO Accounts (Username, Password) VALUES (?, ?)", (details)) # Tuple unpacking if not obvious
            cursor.execute("INSERT INTO BestTimes (Username, Easy, Normal, Hard, 'Extra Hard') VALUES (?, NULL, NULL, NULL, NULL)", (details[0],)) # Tuple unpacking if not obvious

            self.client.send("valid".encode())
            conn.commit()
            conn.close()
            print(f"[Account created with username: {details[0]} from {self.address}]")
            return True

    def login(self):
        print(f"[Login request from {self.address}]")
        self.client.send("proceed".encode())
        details = self.client.recv(1024).decode().split(",")
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        if self.verify(details[0], details[1], cursor):
            print(f"[Successful login by {details[0]} from {self.address}]")
            self.client.send("valid".encode())
            conn.close()
            return True
        else:
            self.client.send("invalid".encode())
            print(f"[Unsuccessful login by {details[0]} from {self.address}]")
            conn.close()
            return False

    def update_BestTimes(self):
        print(f"[Update best times request from {self.address}]")
        self.client.send("proceed".encode())
        times = self.client.recv(1024).decode().split(",")

        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE BestTimes SET Easy = ?, Normal = ?, Hard = ?, 'Extra Hard' = ? WHERE Username = ?", 
                           (times[1], times[2], times[3], times[4], times[0]))
            self.client.send("valid".encode())
            print(f"[Succesfully updated best times from {self.address}]")

        except Exception as e:
            print(f"Error updating best times {e} from {self.address}")
            self.client.send("invalid".encode())

        self.username = times[0]
        self.bestTimes = times[1:]

        conn.commit()
        conn.close()



    def match_Players(self):
        print(f"[Matching request from {self.address}]")
        self.client.send("proceed".encode())
        self.difficulty = self.client.recv(1024).decode()

        if queueDict[self.difficulty].isEmpty():
            pass
            #client.send("Queue empty".encode())
            #prompt use that queue is empty so they mayhave to wait a while

        if queueDict[self.difficulty].enQueue(self):
            print(f"[Enqueued into {self.difficulty} queue {self.username} from {self.address}]")
            self.client.send("Enqueued".encode())
            self.matching = True
            self.startMatchingTime = time.time()
            #wait

        else:
            print(f"[{self.difficulty} queue is full for {self.username} from {self.address}]")
            self.client.send("Queue full".encode())
            #return False


#######################################################################

class Game(threading.Thread):
    def __init__(self, thread1, thread2, difficulty):
        super().__init__()
        self.player1 = thread1
        self.player2 = thread2

        self.puzzleString = self.import_Puzzle(difficulty)
        p = Puzzle(self.puzzleString)
        p.show_Grid()
        p.solve()
        self.solutionString = p.grid_To_String()


    def run(self):
        finished = False
        self.player1.client.send("Match Found".encode())
        self.player2.client.send("Match Found".encode())
        
        self.player1.client.send(self.puzzleString.encode())
        self.player2.client.send(self.puzzleString.encode())

        self.player1.client.send(self.player2.username.encode())
        self.player2.client.send(self.player1.username.encode())

        while finished is False:
            p1Grid = self.player1.client.recv(1024).decode()
            p2Grid = self.player2.client.recv(1024).decode()
            print(f"Player1's grid: [{p1Grid}]")
            print(f"Player2's grid: [{p2Grid}]")
            print()

            if p1Grid == "WIN":
                self.player2.client.send("LOSE".encode())
                finished = True
                self.player1.inGame = False
                self.player2.inGame = False

            elif p2Grid == "WIN":
                self.player1.client.send("LOSE".encode())
                finished = True
                self.player1.inGame = False
                self.player2.inGame = False
                
            elif p1Grid == "QUIT":
                self.player2.client.send("OPPONENT QUIT".encode())
                finished = True
                self.player1.inGame = False
                self.player2.inGame = False
                
            elif p2Grid == "QUIT":
                self.player1.client.send("OPPONENT QUIT".encode())
                finished = True
                self.player1.inGame = False
                self.player2.inGame = False

            else:
                self.player1.client.send(self.compare_Puzzles(p2Grid).encode())
                self.player2.client.send(self.compare_Puzzles(p1Grid).encode())


    def import_Puzzle(self, difficulty):
        with open(f"Main\Generator\{difficulty}.txt", "r") as file:
            puzzles = file.readlines()
            return random.choice(puzzles)


    def compare_Puzzles(self, puzzleString):
        #Makes a string of 1s and 0s, 1s showing correctly filled cells and 0s showing empty and incorrect cells
        return "".join(["1" if puzzleString[i] == self.solutionString[i] else "0" for i in range(81)])

####################################################################################################################################

def create_Match():
    while True:
        time.sleep(1)
        for difficulty in queueDict:
            if not queueDict[difficulty].isEmpty() and queueDict[difficulty].isEven():
                player1 = queueDict[difficulty].deQueue()
                player2 = queueDict[difficulty].deQueue()

                player1.matching, player2.matching = False, False
                player1.inGame, player2.inGame = True, True

                Game(player1, player2, difficulty).start()

                print(f"[Have matched some players {player1.username} from {player1.address} and {player2.username} from {player2.address}]")

###########################################################################################################################################

######################################################################################
################___INITIALISATION___##################################################

host = "127.0.0.1"
port = 7777
DATABASE = "Server\Sudoku_Online.db"

easyQ = Queue(25)
normalQ = Queue(25)
hardQ = Queue(25)
extraHardQ = Queue(25)
queueDict = {"easy": easyQ, "normal": normalQ, "hard": hardQ, "extraHard": extraHardQ}

#######################################################################################

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    threading.Thread(target = create_Match).start()

    while True:
        print("ACCEPTING NEW CONNECTIONS")
        client, address = server.accept()

        print(f"CONNECTION ACCEPTED FROM {address}")
        Client(client, address).start()


if __name__ == "__main__":
    print("__SERVER STARTED__")
    main()


