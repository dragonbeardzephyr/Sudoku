import random
import time
import copy  

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


    def insert(self, row, col, n):
        self.grid[row][col] = n


    def find_Empty_Space(self) -> tuple | None:
        for emptySpace in self.sortedCandidates:
            return emptySpace
        else:
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
        for i in range(9):
            if n in self.candidates[row][i]:
                self.candidates[row][i].remove(n)

            if n in self.candidates[i][col]:
                self.candidates[i][col].remove(n)

        boxRow = row // 3 * 3
        boxCol = col // 3 * 3

        for i in range(boxRow, boxRow+3):
            for j in range(boxCol, boxCol+3):
                if n in self.candidates[i][j]:
                    self.candidates[i][j].remove(n)


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
            if self.check(row, i, n):
                self.candidates[row][i].add(n)

            if self.check(i, col, n):
                self.candidates[i][col].add(n)

        for i in range(boxRow, boxRow+3):
            for j in range(boxCol, boxCol+3):
                if self.check(row, col, n):
                    self.candidates[row][col].add(n)


#############################################################################################################################

    def constraint_Propagation(self):
        self.get_All_Candidates()
        self.sort_Candidates()
        return self.eliminate()


    def eliminate(self):
        if self.find_Empty_Space() == None:
            return True
        
        for emptySpace in self.sortedCandidates.copy():
            if len(emptySpace[0]) == 1:
                #Meaning there is only one possible number that can be placed into the grid,
                self.insert(emptySpace[1], emptySpace[2], self.candidates[emptySpace[1]][emptySpace[2]].pop())
                self.update_Peers_Remove_Candidates(emptySpace[1], emptySpace[2], self.grid[emptySpace[1]][emptySpace[2]])
                
                if self.find_Empty_Space() == None:
                    return True
                
                self.sort_Candidates()
                return self.eliminate()

        return False
    
            
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
        
        
    """
    def dfs(self) -> bool:#Named after Depth First Search, basic backtracking algorithm
        pos = self.find_Empty_Space()#pos is given as a tuple (row, col)
        if pos == None:
            #Meaning the grid is full and solved
            return True

        row, col = pos
        for n in self.candidates[row][col]:
                        
            if self.check(row, col, n):

                self.insert(row, col, n)
                self.update_Peers_Remove_Candidates(row, col, n)
                
                if self.dfs():
                    #Causes all the recursion to unwind
                    return True

                self.insert(row, col, 0)
                #self.update_Peers_Insert_Candidates(row, col, n)

        return False
    """
    def dfs(self) -> bool:#Named after Depth First Search
        emptySpace = self.find_Empty_Space()
        
        if emptySpace == None:
            #Meaning the grid is full and solved
            return True
        
        #emptySpace is given as a (candidates, row, col)
        candidates, row, col = emptySpace

        for n in candidates:
            if self.check(row, col, n):

                self.insert(row, col, n)
                self.sortedCandidates.remove(emptySpace)
                self.update_Peers_Remove_Candidates(row, col, n)
                self.sort_Candidates()
                
                if self.dfs():
                    #Causes all the recursion to unwind
                    return True
                
                self.insert(row, col, 0)
                self.sortedCandidates.insert(0, emptySpace)
                self.update_Peers_Insert_Candidates(row, col, n)
                

        return False
    

    def solve(self):
        if self.constraint_Propagation() == False:
            self.show_grid()
            if self.dfs() == True:
                print("[Solved with DFS]")
                return True
            else:
                print("[Unsolvable]")
                return False
        else:
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
        emptySpace = self.find_Empty_Space()#pos is given as a tuple (row, col)

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
                #if all required number of cells to be removed have been removed
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
        self.duplicates = 0
        
        if mode == "read":
            self.file = open(file, "r")
            self.contents = self.file.readlines()
            self.file.close()

        elif mode == "append":
            self.file = open(file, "a+")
            self.contents = self.file.readlines()

            for puzzleString in data:
                if not f"{puzzleString}\n" in self.contents:
                    self.file.write(f"{puzzleString}\n")
                else:
                    self.duplicates += 1

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


###############################################################################################################################
"""puzzle1 = Puzzle()
#puzzle1.get_All_Candidates()
#print(puzzle1.candidates)
x = time.time()
puzzle1.solve()
y = time.time()
print("1", y-x)

puzzle2 = Puzzle()
x = time.time()
puzzle2.solve()
y = time.time()
print("2", y-x)
"""

"""puzzle3 = puzzle()
print(puzzle3.solveH())
puzzle3.show_Grid()"""


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


if __name__ == "__main__":
    numberToGenerate = 1000 #n*8 puzzles will be generated
    easy = []
    normal = []
    hard = []
    extra_hard = []
    outliers = []
    listOfPuzzles = []

    startTime = time.perf_counter()
    for i in range(numberToGenerate):
        print(f"Puzzle {i+1}")
        listOfPuzzles.append(Puzzle())
    elapsedTime = time.perf_counter() - startTime

    print(f"{round(elapsedTime, 2)} seconds to generate {numberToGenerate} puzzles")

    for puzzle in listOfPuzzles:
        if puzzle.clues in range(17, 28):
            a = make_More(puzzle.grid)
            for i in a:
                extra_hard.append(Puzzle(i).grid_To_String())

        elif puzzle.clues in range(28, 32):
            a = make_More(puzzle.grid)
            for i in a:
                hard.append(Puzzle(i).grid_To_String())

        elif puzzle.clues in range(32, 36):
            a = make_More(puzzle.grid)
            for i in a:
                normal.append(Puzzle(i).grid_To_String())

        elif puzzle.clues in range(36, 45):
            a = make_More(puzzle.grid)
            for i in a:
                easy.append(Puzzle(i).grid_To_String())

        else:
            outliers.append(puzzle.grid_To_String())

    easyFile = PuzzleFile("Main/Generator/easy.txt", "append", easy)
    normalFile = PuzzleFile("Main/Generator/normal.txt", "append", normal)
    hardFile = PuzzleFile("Main/Generator/hard.txt", "append", hard)
    extra_HardFile = PuzzleFile("Main/Generator/extra_hard.txt", "append", extra_hard)

    print(f"easy        {len(easy)}")
    print(f"normal      {len(normal)}")
    print(f"hard        {len(hard)}")
    print(f"extra hard  {len(extra_hard)}")
    print(f"outliers    {len(outliers)}")
    print(f"Total       {numberToGenerate*8}")
    print(f"Duplicates  {easyFile.duplicates + normalFile.duplicates + 
                        hardFile.duplicates + extra_HardFile.duplicates}")


    print(outliers)
    print()
    