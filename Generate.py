import random
import time


class puzzle:
    def __init__(self):
        self.grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
        #self.grid = [[0 for i in range(9)] for j in range(9)]
        self.candidates = [[[] for i in range(9)] for j in range(9)]
        self.emptySpaces = []


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

                
    def find_Empty_SpaceH(self):
        pass
            

    def check(self, row, col, num):#return false if there are any mistakes
        """COMPLETE"""
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
        """COMPLETE"""
        #x = input()#used as next button as to slow down and inspect algorithm
        
        
        pos = self.find_Empty_Space()
        if pos == None:
            return True
    

        row, col = pos[0], pos[1]

        #self.show_grid()
        #print(f"Pos: {pos}")
        #print()

        for n in range(1, 10):

            if self.check(row, col, n):
                self.insert(row, col, n)
                
                if self.solve():
                    return True
                
                self.insert(row, col, 0)#if a solve does not happen then position goes back to zero in case further backtracking needed

        return False
    
    def get_Candidates(self, row, col):
        candidates = set(range(1,10))
        
        candidates -= set(self.grid[row])
    
        candidates -= set(self.grid[i][col] for i in range(9))

        boxRow = row // 3 * 3
        boxCol = col // 3 * 3
        
        candidates -= set(self.grid[i][j] for j in range(boxCol, boxCol+3) for i in range(boxRow, boxRow+3)) 
        return candidates

    def get_All_Candidates(self):

        for row in range(9):
            for col in range(9):
                candidates = set(range(1,10))
              
                candidates -= set(self.grid[row])
           
                candidates -= set(self.grid[i][col] for i in range(9))
  
                boxRow = row // 3 * 3
                boxCol = col // 3 * 3
                
                candidates -= set(self.grid[i][j] for j in range(boxCol, boxCol+3) for i in range(boxRow, boxRow+3)) 
                self.candidates[row][col] = candidates
                #print(self.candidates)
                





    def solveH(self):#Heuristic approach to solve

        #x = input()#used as next button as i am testign right now

        pos = self.find_Empty_Space()
        if pos == None:
            return True
        row, col = pos[0], pos[1]

        #self.show_grid(
        #print(f"Pos: {pos}")
        #print()

        for n in self.get_Candidates(row, col):

            #if self.check(row, col, n):
            self.insert(row, col, n)
                
            if self.solveH():
                return True
                
            self.insert(row, col, 0)#if a solve does not happen then position goes back to zero in case further backtracking needed
    
        return False

    def generate(self):
        pass



puzzle1 = puzzle()
x = time.time()
puzzle1.solve()
y = time.time()
print("1", y-x)

puzzle2 = puzzle()
x = time.time()
puzzle2.solveH()
y = time.time()
print("2", y-x)

#puzzle1.show_grid()
#puzzle2.show_grid()
    

"""puzzle3 = puzzle()
print(puzzle3.solveH())
puzzle3.show_grid()"""
