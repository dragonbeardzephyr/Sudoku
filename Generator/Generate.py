import random
import time
import copy

class Puzzle:

    def __init__(self, string = None):
        if string:#For importing grids
            self.string_To_Grid(string) # Converts a string representation of a puzzle into a 2d array
            self.get_All_Candidates() # Sets candidates for all cells
        else: # Default
            self.generate()

    def show_grid(self):
        for i in self.grid:
            for j in i:
                print(j, end = "  ")
            print()
        print()

    def insert(self, row, col, n):
        self.grid[row][col] = n
        
    def find_Empty_Space(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return (row, col)
        return None

    def check(self, row, col, num):#return false if there are any mistakes

        if num in self.grid[row]:
            return False
        
        for i in range(9):
            if num == self.grid[i][col]:
                return False
        
        boxRow = row // 3 * 3
        boxCol = col // 3 * 3

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

    def get_All_Candidates(self):
        self.candidates = [[set(range(1, 10))for i in range(9)]for j in range(9)]

        for row in range(9):
            for col in range(9):
                if self.grid[row][col] != 0:
                    self.candidates[row][col] = set()

                else:
                    candidates = set(range(1,10))
                
                    candidates -= set(self.grid[row])
            
                    candidates -= set(self.grid[i][col] for i in range(9))
    
                    boxRow = row // 3 * 3
                    boxCol = col // 3 * 3
                    
                    candidates -= set(self.grid[i][j] for j in range(boxCol, boxCol+3) for i in range(boxRow, boxRow+3)) 
                    self.candidates[row][col] = candidates


    def update_Peers_Remove_Candidates(self, row, col):#When a number is inserted, the units that the number is in have their candidates updated
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


    def update_Peers_Insert_Candidates(self, row, col, n):
        #For the cel
        candidates = set(range(1,10))
    
        candidates -= set(self.grid[row])

        candidates -= set(self.grid[i][col] for i in range(9))

        boxRow = row // 3 * 3
        boxCol = col // 3 * 3
        
        candidates -= set(self.grid[i][j] for j in range(boxCol, boxCol+3) for i in range(boxRow, boxRow+3))

        self.candidates[row][col] = candidates

        #For the peers of the cell
        for i in range(9):
            if self.check(row, i, n):
                self.candidates[row][i].add(n)

            if self.check(i, col, n):
                self.candidates[i][col].add(n)
        
        for i in range(boxRow, boxRow+3):
            for j in range(boxCol, boxCol+3):
                if self.check(row, col, n):
                    self.candidates[row][col].add(n)

    def eliminate(self):
        self.get_All_Candidates()
        
        for row in range(9):
            for col in range(9):
                if len(self.candidates[row][col]) == 1:#Meaning there is only one possible number that can be placed into the grid,
                    self.insert(row, col, self.candidates[row][col].pop())#So it is
                    #self.update_Peers_Remove_Candidates(row, col, self.grid[row][col])

                
    def dfs(self):#depth first search of solvign a sudoku grid, brute force method of solvign a grid
        #x = input()#used as next button as to slow down and inspect algorithm
        pos = self.find_Empty_Space()#pos is given as a tuple (row, col)
        if pos == None:#Meaning the grid is full and solved
            return True
        
        row, col = pos[0],pos[1]

        #self.show_grid()
        #print(f"Pos: {pos}")
        #print()
        #candidates = copy.deepcopy(self.candidates[row][col])
        for n in self.candidates[row][col]:

            if self.check(row, col, n):

                self.insert(row, col, n)

                #self.update_Peers_Remove_Candidates(row, col ,n)
                
                if self.dfs(): #Causes all the recursion to unwind
                    return True

                self.insert(row, col, 0)

                #self.update_Peers_Insert_Candidates(row, col, n)

        return False


    def solve(self):
        self.eliminate()
        return self.dfs()#Return is used to just cehck for the true false part of statement

##############################################################################################################################

    def fill_Grid(self):
        print("Filling Grid")
        solved = False#Initialises it for while loop

        while solved == False:
            
            self.grid = [[0 for col in range(9)] for row in range(9)]#Wipes grid clean

            count = {}
            for n in range(1, 10):#Will be used to count how many of each number is inserted
                count[n] = 0

            n = random.randint(25, 35)#Arbitrary

            while n > 0 :
                x = random.randint(1, 9)
                row = random.randint(0, 8)
                col = random.randint(0, 8)

                if self.grid[row][col] == 0:
                    if self.check(row, col, x) and count[x] < 9:#Mkaes sure that no more than 9 copies of the same number are in the grid
                        self.insert(row, col, x)
                        count[x] += 1

                        n -= 1

            solved = self.solve()


    def count_Solutions(self):#Copy of DFS solve function, but instead is designed to perform a full search for all solutions, however this version is capped to stop at two solutions
        #print("Counting Solutions")
        
        pos = self.find_Empty_Space()#pos is given as a tuple (row, col)

        if pos == None:#Meaning the grid is full and solved
            self.solutions += 1 #Just notes that it has reached a solotion and looks for others
            return #Continues "EXPLORING" grid for more solutions
        
        row, col = pos[0],pos[1]

        #candidates = copy.deepcopy(self.candidates[row][col])
        for n in range(1, 10):
            if self.check(row, col, n):

                self.insert(row, col, n)
                #self.update_Peers_Remove_Candidates(row, col , n)

                self.count_Solutions()

                if self.solutions > 1:#As soon as more than one solution is found we know the grid isnt unique and stops searching
                    return
                
                self.insert(row, col, 0)
                #self.update_Peers_Insert_Candidates(row, col, n)



        

    def remove_digits(self):
        self.solutions = 0
        #k = random.randint(36, 64)
        k = int(random.triangular(36, 64, 50))#Randomly generates between 36 and 64 and is weighted to generate closer to 50.
        x = 0 #Used to count how many digits have been removed
        change = copy.deepcopy(self.grid)#Will store up to date grid, as self.solve() affects self.grid
        cells = [(row, col) for col in range(9) for row in range(9)]*3#All locations
        random.shuffle(cells)

        for row, col in cells:#While all cells haven't been visited

            n = self.grid[row][col]
            self.insert(row, col, 0)

            change = copy.deepcopy(self.grid)

            self.count_Solutions()

            if self.solutions > 1:#If more than one solutions are found, undo removal of digit and break loop
                self.grid = copy.deepcopy(change)
                self.insert(row, col, n)
                self.solutions = 0

            else:
                self.grid = copy.deepcopy(change)
                x += 1

            if x == k:#if all required number of cells to be removed have been removed
                break

        self.grid = copy.deepcopy(change)
        return 81 - x #number of cells removed


    def generate(self):
        self.fill_Grid()
        #self.show_grid()
        self.clues = self.remove_digits()
        #print(f"Clues: {self.clues}")
        #self.show_grid()

    def rotate_FLip_grid(self):#Fucntion to make more grids out of already existing ones via rotating and flipping them, not neccessary.
        pass

##############################################################################################################################

    def grid_To_String(self):#Will convert the grid into a string that can be saved on a file
        return "".join( ["".join( [str(item) for item in row] ) for row in self.grid] )
    
    def string_To_Grid(self, string):
        #the if statement accounts for some Sudoku grids that have a dot representing the empty space instead of 0
        self.grid = [[int(item) if item != "." else 0 for item in string[9*row:9*(row+1)]] for row in range(len(string)//9)]

##############################################################################################################################


class PuzzleFile:
    def __init__(self, file, mode, data = None):
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

        else:
            return ValueError

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
#puzzle1.show_grid()
#puzzle2.show_grid()
    

"""puzzle3 = puzzle()
print(puzzle3.solveH())
puzzle3.show_grid()"""

"""MAIN PROGRAM"""

n = 10
easy = []
normal = []
hard = []
extra_hard = []
outliers = []

listOfPuzzles = []

y = time.time()

for i in range(n):
    print(f"Puzzle {i+1}")
    listOfPuzzles.append(Puzzle())

x = time.time()

print(f"{x-y} seconds to generate {n} puzzles")

for p in listOfPuzzles:
    if p.clues in range(17, 28):
        extra_hard.append(p.grid_To_String())
    elif p.clues in range(28, 32):
        hard.append(p.grid_To_String())
    elif p.clues in range(32, 36):
        normal.append(p.grid_To_String())
    elif p.clues in range(36, 45):
        easy.append(p.grid_To_String())
    else:
        outliers.append(p.grid_To_String())

print(f"easy        {len(easy)}")
print(f"normal      {len(normal)}")
print(f"hard        {len(hard)}")
print(f"extra hard  {len(extra_hard)}")
print(f"outliers    {len(outliers)}")

easyFile = PuzzleFile("Generator/easy.txt", "append", easy)
normalFile = PuzzleFile("Generator/normal.txt", "append", normal)
hardFile = PuzzleFile("Generator/hard.txt", "append", hard)
extra_HardFile = PuzzleFile("Generator/extra_hard.txt", "append", extra_hard)

print(outliers)

