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
    
##############################################################################################################################

    def fill_Grid(self):
        solved = False

        while solved == False:
            self.grid = [[0 for col in range(9)] for row in range(9)]

            count = {}
            for n in range(1, 10):
                count[n] = 0

            n = random.randint(25, 40)

            while n > 0 :
                x = random.randint(1, 9)
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                if self.check(row, col, x) and count[x]<10:#Mkaes sure that no more than 9 
                    self.insert(row, col, x)
                    count[x] += 1

                n -= 1

            solved = self.solve()

    def remove_digits(self, k = random.randint(35, 64)):
        print("remove_digits")
        print(k)
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
        return 81-(x-k)#number of cells removed

    def generate(self):
        self.fill_Grid()
        clues = self.remove_digits()
        self.show_grid()
        print(clues)

##############################################################################################################################

    def grid_To_String(self):#Will convert the grid into a string that can be saved on a file
        string = ""
        for row in self.grid:
            for item in row:
                string += str(item)

        return string
    
    def string_To_Grid(self):
        #the if statement accounts for some Sudoku grids that have a dot representing the empty space instead of 0
        self.grid = [[item if item != "." else "0" for item in string[9*row:9*(row+1)]] for row in range(len(string)//9)]

##############################################################################################################################

difficulty = {1:"easy.txt",2:"normal.txt",3:"hard.txt",4:"extra_hard.txt"}

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
                    self.file.append(puzzleString)
            
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


p4 = Puzzle()
#l = [Puzzle() for i in range(10)]
#for i in l:
#    l.show_grid()