import time
import cProfile
import random
import copy
import sys

print("""

             ██████╗██╗   ██╗██████╗  █████╗ ██╗  ██╗██╗   ██╗
            ██╔════╝██║   ██║██╔══██╗██╔══██╗██║ ██╔╝██║   ██║
            ╚█████╗ ██║   ██║██║  ██║██║  ██║█████═╝ ██║   ██║
             ╚═══██╗██║   ██║██║  ██║██║  ██║██╔═██╗ ██║   ██║
            ██████╔╝╚██████╔╝██████╔╝╚█████╔╝██║ ╚██╗╚██████╔╝
            ╚═════╝  ╚═════╝ ╚═════╝  ╚════╝ ╚═╝  ╚═╝ ╚═════╝ 

             ██████╗ ███████╗███╗  ██╗███████╗██████╗  █████╗ ████████╗ █████╗ ██████╗ 
            ██╔════╝ ██╔════╝████╗ ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗
            ██║  ██╗ █████╗  ██╔██╗██║█████╗  ██████╔╝███████║   ██║   ██║  ██║██████╔╝
            ██║  ╚██╗██╔══╝  ██║╚████║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║  ██║██╔══██╗
            ╚██████╔╝███████╗██║ ╚███║███████╗██║  ██║██║  ██║   ██║   ╚█████╔╝██║  ██║
             ╚═════╝ ╚══════╝╚═╝  ╚══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚════╝ ╚═╝  ╚═╝
        """)

print([].pop(0))

def time_taken(func):
    st = time.perf_counter()
    result = func()
    et = time.perf_counter()
    return et-st, result


class Puzzle:
    def __init__(self, data : str | list | None = None):
        if type(data) == str:#For importing grids
            self.string_To_Grid(data) # Converts a string representation of a puzzle into a 2d array
            self.get_All_Candidates() # Sets candidates for all cells

        elif type(data) == list: # For importing grid as 2d array, used for converting grid into string
            self.grid = data

        else: # Default
            self.generate()


    def show_grid(self):
        for row in self.grid:
            for item in row:
                print(item, end = "  ")
            print()#newline
        print()

    def show_Candidates(self):
        for row in self.candidates:
            for item in row:
                print(item, end = "  ")
            print()
            
    def insert(self, row, col, n):
        self.grid[row][col] = n


    def find_Empty_Space_Sorted(self) -> tuple | None:
        return self.sortedCandidates[0] if len(self.sortedCandidates) > 0 else None

    def find_Empty_Space(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return (row, col)
        return None

    def check(self, row : int, col : int, num : int) -> bool:#return false if there are any mistakes

        if num in self.grid[row]:
            return False

        for i in range(9):
            if num == self.grid[i][col]:
                return False

        boxRow = row // 3 * 3 #Reduces numbers to either 0, 3 or 6 the
        boxCol = col // 3 * 3 #starting indexes for a cells respective box

        for i in range(boxRow, boxRow+3):
            for j in range(boxCol, boxCol+3):
                if num == self.grid[i][j]:
                    return False

        return True


    """
    def solve(self):#Basic DFS Solve function

        pos = self.find_Empty_Space()
        if pos == None:
            return True

        row, col = pos[0], pos[1]

        for n in range(1, 10):

                if self.check(row, col, n):
                    self.insert(row, col, n)

                    if self.solve():
                        return True

                    self.insert(row, col, 0)#if a solve does not happen then position goes back to zero in case further backtracking needed

            return False
    """


    def get_All_Candidates(self):#
        self.candidates = [[set() for i in range(9)]for j in range(9)]
        #All cells start with empty candidates set
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    #If cell is empty then it will get all possible candidates
                    candidates = set(range(1,10))

                    candidates -= set(self.grid[row])

                    candidates -= set(self.grid[i][col] for i in range(9))

                    boxRow = row // 3 * 3
                    boxCol = col // 3 * 3

                    candidates -= set(self.grid[i][j]
                                    for j in range(boxCol, boxCol+3)
                                    for i in range(boxRow, boxRow+3))

                    self.candidates[row][col] = candidates
                
    def sort_Candidates(self):
        self.sortedCandidates = sorted( [(self.candidates[row][col], row, col) for col in range(9) for row in range(9) if len(self.candidates[row][col]) > 0], key = lambda x: len(x[0]) )


###########################_EXPERIMENTAL_CODE_############################################################################################
    #number is removed
    def update_Peers_Remove_Candidates(self, row : int, col : int, n : int):#When a number is inserted, the cells in the same row, column and box will have that number removed from their candidates
        self.candidates[row][col] = set()
        
        for i in range(9):
            self.candidates[row][i].discard(n)

            self.candidates[i][col].discard(n)

        boxRow = row // 3 * 3
        boxCol = col // 3 * 3

        for i in range(boxRow, boxRow+3):
            for j in range(boxCol, boxCol+3):
                self.candidates[i][j].discard(n)


    def update_Peers_Insert_Candidates(self, row : int, col : int, n : int):
        #For adding candidates back to a cell that was previously filled
        candidates = set(range(1,10))

        candidates -= set(self.grid[row])

        candidates -= set(self.grid[i][col] for i in range(9))

        boxRow = row // 3 * 3
        boxCol = col // 3 * 3

        candidates -= set(self.grid[i][j] for j in range(boxCol, boxCol+3) for i in range(boxRow, boxRow+3))

        self.candidates[row][col] = candidates

        #For the peers of the cell adds the number back to their candidates
        for i in range(9):
            if self.grid[row][i] == 0 and self.check(row, i, n):
                self.candidates[row][i].add(n)

            if self.grid[i][col] == 0 and self.check(i, col, n):
                self.candidates[i][col].add(n)

        for i in range(boxRow, boxRow+3):
            for j in range(boxCol, boxCol+3):
                if self.check(i, j, n):
                    self.candidates[i][j].add(n) if self.grid[i][j] == 0 else None


#############################################################################################################################

    def constraint_Propagation(self):
        self.get_All_Candidates()
        self.sort_Candidates()
        return self.eliminate()


    def eliminate(self):
        while self.find_Empty_Space_Sorted() != None:
            candidates, row, col = self.find_Empty_Space_Sorted()
            if len(candidates) == 1:
                #Meaning there is only one possible number that can be placed into the grid,
                
                self.insert(row, col, candidates.pop())
                self.update_Peers_Remove_Candidates(row, col, self.grid[row][col])
                self.sort_Candidates()
                
            elif len(candidates) == 0:
                return "Invalid"
                
            else:
                break#If there are no cells with only one candidate, then break out of the loop and resort to backtrakcign to solve the rest
        
        else:
            return "Solved"#Runs if while condition is met
        
        return "Unsolved"
    
            
        """
        for row in range(9):
            for col in range(9):
                if len(self.candidates[row][col]) == 1:
                    #Meaning there is only one possible number that can be placed into the grid,
                    self.insert(row, col, self.candidates[row][col].pop())
                    self.update_Peers_Remove_Candidates(row, col, self.grid[row][col])
                    
                    if self.find_Empty_Space() == None:
                        return True
                    else:
                        return self.eliminate()
        
        return False
        """
        
    def dfs(self) -> bool:#Named after Depth First Search, basic backtracking algorithm
        emptySpace = self.find_Empty_Space_Sorted()#pos is given as a tuple (row, col)
        if emptySpace == None:
            #Meaning the grid is full and solved
            return True

        candidates, row, col = emptySpace
        
        for n in candidates:
                        
            if self.check(row, col, n):

                self.insert(row, col, n)
                #self.update_Peers_Remove_Candidates(row, col, n)
                self.sortedCandidates.remove(emptySpace)
                
                if self.dfs():
                    #Causes all the recursion to unwind
                    return True

                self.insert(row, col, 0)
                self.sortedCandidates.insert(0, emptySpace)
                #self.update_Peers_Insert_Candidates(row, col, n)

        return False


    def solve(self):
        if self.constraint_Propagation() == "Unsolved":
            self.show_grid()
            
            if self.dfs() == True:
                print("[Solved with DFS]")
                return True
            else:
                print("[Unsolvable]")
                return False
            
        elif self.constraint_Propagation() == "Invalid":
            print("[Unsolvable]")
            return False
        
        elif self.constraint_Propagation() == "Solved":
            print("[Solved with Constraint Propagation]")
            return True
        #return self.dfs()

    ##############################################################################################################################


    def fill_Grid(self):
        print("[Filling Grid]")
        solved = False

        while solved == False:

            self.grid = [[0 for col in range(9)] for row in range(9)]

            count = {}
            for i in range(1, 10):
                #Will be used to keep track of how many of each number is inserted
                count[i] = 0

            numberOfCellsToInsert = random.randint(25, 35)

            while numberOfCellsToInsert > 0 :
                x = random.randint(1, 9)
                row = random.randint(0, 8)
                col = random.randint(0, 8)

                if self.grid[row][col] == 0:
                    if count[x] < 9 and self.check(row, col, x):
                        #Ensures that no more than 9 copies of the same number
                        self.insert(row, col, x)
                        count[x] += 1

                        numberOfCellsToInsert -= 1

            self.get_All_Candidates()
            self.sort_Candidates()
            solved = self.dfs()


    def count_Solutions(self):
        #print("[Counting Solutions]")
        emptySpace = self.find_Empty_Space_Sorted()#pos is given as a tuple (row, col)

        if emptySpace == None:#Meaning the grid is full and solved
            self.solutions += 1 #Notes that it has found a solution
            return #Continues "EXPLORING" grid for more solutions

        candidates, row, col = emptySpace

        for n in candidates:
            if self.check(row, col, n):

                self.insert(row, col, n)
                self.sortedCandidates.remove(emptySpace)
                
                self.count_Solutions()

                if self.solutions > 1:
                    #More than one solution is found so we stop searching
                    return

                self.insert(row, col, 0)
                self.sortedCandidates.insert(0, emptySpace)


    def remove_digits(self):
        print("[Removing Digits]")
        self.solutions = 0
        digitsToRemove = int(random.triangular(36, 64, 50))# Weighted towards 50
        digitsRemoved = 0 #Used to count how many digits have been removed
        change = copy.deepcopy(self.grid)

        cells = [(row, col) for col in range(9) for row in range(9)]*3
        #All locations are set three times so that algorithm does not end too soon
        random.shuffle(cells)

        for row, col in cells:#While all cells haven't been visited thrice

            n = self.grid[row][col]
            self.insert(row, col, 0)

            change = copy.deepcopy(self.grid)

            self.count_Solutions()

            if self.solutions > 1:
                #If more than one solutions are found, undo removal of digit
                self.grid = copy.deepcopy(change)
                self.insert(row, col, n)
                self.solutions = 0

            else:
                self.grid = copy.deepcopy(change)
                digitsRemoved += 1

            if digitsRemoved == digitsToRemove:
                #if all required number of cells to be removed haveS been removed
                break

        self.grid = copy.deepcopy(change)
        self.clues = 81 - digitsRemoved



    def generate(self):
        self.fill_Grid()
        self.remove_digits()
        #print(f"Clues: {self.clues}")

##############################################################################################################################

    def grid_To_String(self) -> str:
        #Will convert the grid into a string that can be saved on a file
        return "".join( ["".join([str(item) for item in row]) for row in self.grid] )

    def string_To_Grid(self, string : str):
        #the if statement accounts for grids that use a dot instead of 0
        self.grid = [[int(item) if item != "." else 0
                    for item in string[9*row:9*(row+1)]]
                    for row in range(9)]

##############################################################################################################################


class PuzzleFile:
    def __init__(self, file : str, mode : str, data : list = []):
        if mode == "read":
            self.file = open(file, "r")
            self.contents = self.file.readlines()
            self.file.close()

        elif mode == "append":
            self.file = open(file, "a+")
            self.contents = self.file.readlines()

            for puzzleString in data:
                if not puzzleString in self.contents:
                    self.file.write(f"{puzzleString}\n")

            self.file.close()

################################################################################################
class Stack():
    def __init__(self, maxSize = 10):
        self.__stack = [None for i in range(maxSize)]
        self.__top = -1
        self.__maxSize = maxSize

    def isFull(self):
        return True if self.__top == self.__maxSize - 1 else False

    def isEmpty(self):
        return True if self.__top == -1 else False


    def pushToStack(self, item):
        if self.isFull():
            print("Stack Full")
        else:
            self.__top += 1
            self.__stack[self.__top] = item


    def popFromStack(self):
        if self.isEmpty():
            print("Stack Empty")
            return None
        else:
            item = self.__stack[self.__top]
            self.__top -= 1
            return item


    def show(self):
        print(self.__stack)



def flip_Vertical(grid : list) -> list:
    a = Stack(9)
    for row in grid:
        a.pushToStack(row)
    return [a.popFromStack() for i in range(9)]

def rotate_90(grid : list) -> list:
    a = [[], [], [], [], [], [], [], [], []]
    for col in range(9):#for each column
         for row in range(8, -1, -1):#for each item in column, going down to up, this transposes the first column to the first row, with the bottom of the column aligned with the start of the row
              a[col].append(grid[row][col])
    return a


def make_More(grid : list) -> list:
    a = []
    a.append(grid)

    flipped = flip_Vertical(grid)
    a.append(flipped)

    for i in range(3): # 90, 180, 270
        grid = rotate_90(grid)
        a.append(grid)

        flipped = rotate_90(flipped)
        a.append(flipped)

    return a



