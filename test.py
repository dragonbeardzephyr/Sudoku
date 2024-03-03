import time
import timeit
import cProfile

def time_taken(func = lambda x: x):
    st = time.time()
    func()
    et = time.time()
    print(et-st)


class Puzzle:

    def __init__(self, string):
        self.string_To_Grid(string)
        self.solutions = 0

    def string_To_Grid(self, string):
        #the if statement accounts for some Sudoku grids that have a dot representing the empty space instead of 0
        self.grid = [[int(item) if item != "." else 0 for item in string[9*row:9*(row+1)]] for row in range(len(string)//9)]

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
    
    def count(self, a = None):
        print(a)
        pos = self.find_Empty_Space()
        print(pos)
        if pos == None:
            self.solutions += 1
            print("FOund SOlution")
            return
        
        row, col = pos

        for n in range(1, 10):
            if self.check(row, col ,n):
                self.insert(row, col, n)
                print("_")
                self.count("hello")
                self.insert(row, col, 0)

