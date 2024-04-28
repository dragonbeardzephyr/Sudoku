import socket
import threading
import sqlite3
import random
import time

from Generator.Generate import Puzzle

host = "127.0.0.1"
port = 7777

DATABASE = "Server\Sudoku_Online.db"



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


class Game(threading.Thread):
    def __init__(self, thread1, thread2, difficulty):
        super().__init__()
        self.player1 = thread1
        self.player2 = thread2
        
        self.puzzleString = self.import_Puzzle(difficulty)
        p = Puzzle(self.puzzleString)
        p.show_grid()
        p.solve()
        self.solutionString = p.grid_To_String()


    def run(self):
        finished = False
        self.player1.client.send("Match Found".encode())
        self.player2.client.send("Match Found".encode())
        self.player1.client.send(self.puzzleString.encode())
        self.player2.client.send(self.puzzleString.encode())

        while not finished:
            p1Grid = self.player1.client.recv(1024).decode()
            p2Grid = self.player2.client.recv(1024).decode()
            print(p1Grid)
            print(p2Grid)
            print()

            if p1Grid == "WIN":
                self.player2.client.send("LOSE".encode())
                finished = True
            elif p2Grid == "WIN":
                self.player1.client.send("LOSE".encode())
                finished = True
            else:
                self.player1.client.send(self.compare_Puzzles(p2Grid).encode())
                self.player2.client.send(self.compare_Puzzles(p1Grid).encode())
            
            

    def import_Puzzle(self, difficulty):
        with open(f"Main\Generator\{difficulty}.txt", "r") as file:
            puzzles = file.readlines()
            return random.choice(puzzles)
        
    def compare_Puzzles(self, puzzleString):#Makes a string of 1s and 0s, 1s showing correctly filled cells and 0s showing empty and incorrect cells
        return "".join(["1" if puzzleString[i] == self.solutionString[i] else "0" for i in range(81)])
           
easyQ = Queue(25)
normalQ = Queue(25)
hardQ = Queue(25)
extraHardQ = Queue(25)
queueDict = {"easy": easyQ, "normal": normalQ, "hard": hardQ, "extraHard": extraHardQ}


def create_Match():
    while True:
        time.sleep(1)
        for difficulty in queueDict:
            if queueDict[difficulty].isEven() and not queueDict[difficulty].isEmpty():
                player1 = queueDict[difficulty].deQueue()
                player2 = queueDict[difficulty].deQueue()
                print(f"Have matched some players {player1.username} and {player2.username}")
                Game(player1, player2, difficulty).start()
                #--> This will start the game thread and execute game.run()


######################################################################

class Client(threading.Thread):
    def __init__(self, client, address):
        super().__init__()
        self.client = client
        self.address = address
        self.username = None
        self.bestTimes = [None, None, None, None]
        self.lock = threading.Lock()
        self.options = { "login": self.login,
                    "register": self.register,
                    "match_Players": self.match_Players,
                    "update_BestTimes" : self.update_BestTimes,
                    "play_Multiplayer": self.play_Multiplayer}
        
        self.difficulty = None
        self.matching = False
        self.startMatchingTime = 0

    def run(self):    
        while True:
            try:

                if self.matching == True:
                    if time.time() - self.startMatchingTime > 300:#After 5 minutes removes player from match queue
                        self.matching = False
                        self.client.send("Match Not Found".encode())
                    continue
                
                else:
                    print(f"Waiting for request from {self.username}")
                    request = self.client.recv(1024).decode()
                    print(request)
                    
                    if not request:
                        print("not request")

                    if request == "Logout":
                        break

                    elif request in self.options:
                        self.options[request]()

            except Exception as e :
                print(f"Inavlid request {e}")
                break


        print("Closing connection")
        self.client.close()

    def check(self, username, cursor):
        result = cursor.execute("SELECT Username FROM Accounts WHERE Username = ?", (username,)).fetchone()
        print(f"result: {result}")   
        if result is None:
            print("username not in database")
            return False
        elif username in result:
            print("username in database")
            return True


    def verify(self, username, password, cursor):#Checks if username an dpassword match
        if self.check(username, cursor):
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
    #######################################################################

    #######################################################################
    #Request Redirections
    #######################################################################
    def register(self):
        print("Doing register stuff on self.client")
        self.client.send("proceed".encode())
        details = self.client.recv(1024).decode().split(",")
        print(details)
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()

        if self.check(details[0], cursor):
            self.client.send("invalid".encode())#USername already exists
            conn.close()
            return False
        
        else:
            cursor.execute("INSERT INTO Accounts (Username, Password) VALUES (?, ?)", (details)) # Tuple unpacking if not obvious
            cursor.execute("INSERT INTO BestTimes (Username, Easy, Normal, Hard, 'Extra Hard') VALUES (?, NULL, NULL, NULL, NULL)", (details[0],)) # Tuple unpacking if not obvious

            self.client.send("valid".encode())
            conn.commit()
            conn.close()
            print("INserted")
            return True
        
    def login(self):
        print("doing login stuff on sever")
        self.client.send("proceed".encode())
        details = self.client.recv(1024).decode().split(",")
        print("1")
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        print("2")
        if self.verify(details[0], details[1], cursor):
            print("3")
            print(f"Login good by {details[0]}")
            self.client.send("valid".encode())
            conn.close()
            return True
        else:
            print("4")
            self.client.send("invalid".encode())
            print("Login bad")# Login badd
            conn.close()
            return False

    def update_BestTimes(self):
        self.client.send("proceed".encode())
        times = self.client.recv(1024).decode().split(",")

        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE BestTimes SET Easy = ?, Normal = ?, Hard = ?, 'Extra Hard' = ? WHERE Username = ?", (times[1], times[2], times[3], times[4], times[0]))
            self.client.send("valid".encode())
            
        except Exception as e:
            print(f"Error updating best times {e}")
            self.client.send("invalid".encode())

        self.username = times[0]
        self.bestTimes = times[1:]

        conn.commit()
        conn.close()
        


    def match_Players(self):
        print("Doing Ma_tching stuff on server")
        self.client.send("proceed".encode())
        self.difficulty = self.client.recv(1024).decode()
        print(self.difficulty)

        if queueDict[self.difficulty].isEmpty():
            print("Empty Queue")
            #client.send("Queue empty".encode())
            #prompt use that queue is empty so they mayhave to wait a while
        
        if queueDict[self.difficulty].enQueue(self):
            print("Enqueued")
            self.client.send("Enqueued".encode())
            self.matching = True
            self.startMatchingTime = time.time()
            #wait
        
        else:
            print("Queue full")
            self.client.send("Queue full".encode())
            #return False

    def play_Multiplayer(self):
        print("Doing multiplayer stuff onserver")
        self.client.send("proceed".encode())
        

#######################################################################

#######################################################################

#######################################################################



#######################################################################
#Handler
#######################################################################

#######################################################################


#######################################################################
#Main
#######################################################################


connections = []

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    
    threading.Thread(target = create_Match).start()
    
    while True:
        print("Waiting for connection")
        client, address = server.accept()
        print(f"Connection from {address}")

        Client(client, address).start()


if __name__ == "__main__":
    main()

