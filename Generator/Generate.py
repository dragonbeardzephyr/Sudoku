import random
import time
import copy

class Puzzle:

    def __init__(self, string = None):
        if string:
            self.grid = self.string_To_Grid(string)
        else:
            self.grid = []
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
    def solve(self):

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

    def eliminate(self):
        self.candidates = [[set(range(1, 10))for i in range(9)]for j in range(9)]
        for row in range(9):
            for col in range(9):

                if self.grid[row][col] == 0:

                    self.candidates[row][col] -= set(self.grid[row])

                    self.candidates[row][col] -= set(self.grid[i][col] for i in range(9))

                    boxRow = row // 3 * 3
                    boxCol = col // 3 * 3

                    self.candidates[row][col] -= set(self.grid[i][j] for j in range(boxCol, boxCol+3) for i in range(boxRow, boxRow+3)) 

        if len(self.candidates[row][col]) == 1:
            self.grid[row][col] = self.candidates[row][col].pop()

    def dfs(self):

        #x = input()#used as next button as to slow down and inspect algorithm
        pos = self.find_Empty_Space()
        if pos == None:
            return True
        row, col = pos[0],pos[1]

        #self.show_grid()
        #print(f"Pos: {pos}")
        #print()

        for n in self.candidates[row][col]:

            if self.check(row, col, n):
                self.insert(row, col, n)
                self.candidates[row][col].remove(n)
                
                if self.dfs():
                    return True

                self.insert(row, col, 0)
                self.candidates[row][col].add(n)

        return False

    def solve(self):
        self.eliminate()
        self.dfs()

##############################################################################################################################

    def fill_Grid(self):
        solved = False

        while solved == False:
            
            self.grid = [[0 for col in range(9)] for row in range(9)]#Wipes grid clean

            count = {}
            for n in range(1, 10):
                count[n] = 0

            n = random.randint(25, 40)

            while n > 0 :
                x = random.randint(1, 9)
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                if self.grid[row][col] == 0:
                    if self.check(row, col, x) and count[x]<9:#Mkaes sure that no more than 9 
                        self.insert(row, col, x)
                        count[x] += 1

                        n -= 1

            solved = self.solve()

    def remove_digits(self):
        #print("remove_digits")
        #print(k)
        k = random.randint(36, 64)
        x = k#x id constant for future calculations
        prime = copy.deepcopy(self.grid)#Original grid
        change = copy.deepcopy(self.grid)#Will store up to date grid, as self.solve() affects self.grid

        while k > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.grid[row][col] != 0:
                n = self.grid[row][col]
                self.insert(row, col, 0)
                #self.show_grid()
                change = copy.deepcopy(self.grid)

                self.solve()
                if self.grid != prime:
                    self.grid = copy.deepcopy(change)
                    self.insert(row, col, n)
                    break

                else:
                    self.grid = copy.deepcopy(change)
                    k -= 1

        self.grid = copy.deepcopy(change)
        return 81-x#number of cells removed

    def generate(self):
        print("fill grid")
        self.fill_Grid()
        print("remove digits")
        self.clues = self.remove_digits()

        self.show_grid()
        print(self.clues)
        print()


##############################################################################################################################

    def grid_To_String(self):#Will convert the grid into a string that can be saved on a file
        string = ""
        for row in self.grid:
            for item in row:
                string += str(item)

        return string
    
    def string_To_Grid(self, string):
        #the if statement accounts for some Sudoku grids that have a dot representing the empty space instead of 0
        self.grid = [[item if item != "." else "0" for item in string[9*row:9*(row+1)]] for row in range(len(string)//9)]

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

n = 200
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
    elif p.clues in range(36, 46):
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