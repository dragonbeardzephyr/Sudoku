import socket
import threading
import sqlite3
import random
import time
from Generator.Generate import Puzzle

host = "127.0.0.1"
port = 7777

DATABASE = "Server\Sudoku_Online.db"

class Account():
     def __init__(self, client, username):
            self.client = client
            self.username = username
            self.bestTimes = [None, None, None, None]


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
		with self.lock:
			return self.__size % 2 == 0
				
			
	def enQueue(self, item):
		with self.lock:
			if self.isFull():
				return item
			else:
				self.__rear = (self.__rear + 1) % self.__maxSize
				self.__queue[self.__rear] = item
				self.__size += 1
				return True
	
			#print(self.__front, self.__rear)

	def deQueue(self):
		with self.lock:
			if self.isEmpty():
				return False
			else:
				data = self.__queue[self.__front]
				self.__front = (self.__front + 1) % self.__maxSize
				self.__size -= 1
				return data
	
			#print(self.__front, self.__rear)
	
	def show(self):
		print()
		for i in range(self.__size):#prints in order
			print(self.__queue[(self.__front + i) % self.__maxSize])


class Game(threading.Thread):
    def __init__(self, thread1, thread2, difficulty):
        super().__init__()
        self.player1 = thread1
        self.player2 = thread2
        
        self.puzzleString = self.import_Puzzle(difficulty)
        p = Puzzle(puzzleString)
        p.solve()
        self.solutionString = p.grid_To_String()


    def run(self):
        finished = False
        self.player1.sendall("")
        self.player2.sendall("")
        while not finished:
            pass

    def import_Puzzle(self, difficulty):
        with open(f"Main\Generator\{difficulty}.txt", "r") as file:
            puzzles = file.readlines()
            return random.choice(puzzles)
        
    def compare_Puzzles(self,)
            
easyQ = Queue()
normalQ = Queue()
hardQ = Queue()
extraHardQ = Queue()
queueDict = {"easy": easyQ, "normal": normalQ, "hard": hardQ, "extraHard": extraHardQ}


def create_Match():
    for difficulty in queueDict:
        if queueDict[difficulty].isEven() and not queueDict[difficulty].isEmpty():
            player1 = queueDict[difficulty].deQueue()
            player2 = queueDict[difficulty].deQueue()
            game = Game(player1, player2, difficulty)
            game.start()#--> This will start the game thread and execute game.run()


#######################################################################
#Database Functions
#######################################################################
db_lock = threading.Lock()

def check(username, cursor):
    with db_lock:
        result = cursor.execute("SELECT Username FROM Accounts WHERE Username = ?", (username,)).fetchone()
        print(f"result: {result}")   
        if result is None:
            print("username not in database")
            return False
        elif username in result:
            print("username in database")
            return True


def verify(username, password, cursor):#Checks if username an dpassword match
    with db_lock:#ensures only on thread can
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
#######################################################################



#######################################################################
#Request Redirections
#######################################################################
def register(client):
    print("Doing register stuff on client")
    client.sendall("proceed".encode())
    details = client.recv(1024).decode().split(",")
    print(details)
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
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

    conn = sqlite3.connect(DATABASE, check_same_thread=False)
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

    conn = sqlite3.connect(DATABASE, check_same_thread=False)
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

    if queueDict[difficulty].isEmpty():
        client.send("Queue empty".encode())
        #prompt use that queue is empty so they mayhave to wait a while
    
    if queueDict[difficulty].enQueue(client):
        print("Enqueued")
        #return True
    
    else:
        print("Queue full")
        client.sendall("Queue full".encode())
        #return False

def play_Multiplayer(client):
    print("Doing login stuff on client")

#######################################################################

#######################################################################
options = {"login": login,
        "register": register,
        "match_Players": match_Players,
        "update_BestTimes" : update_BestTimes}
#######################################################################



#######################################################################
#Handler
#######################################################################
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
#######################################################################


#######################################################################
#Main
#######################################################################
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    while True:

        client, address = server.accept()
        print(f"Connection from {address}")

        thread = threading.Thread(target = handle, args = (client, address))
        thread.start()

        print("pong")
        
        create_Match()




if __name__ == "__main__":
    main()

