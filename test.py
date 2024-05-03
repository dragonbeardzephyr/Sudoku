from re import I
import time
import timeit
import cProfile
import random
import copy
import sys


def time_taken(func):
    st = time.perf_counter()
    result = func()
    et = time.perf_counter()
    return et-st, result

#time_taken(lambda: print("Hello World!"))


"""
string = "".join([str(i) for i in range(81)])
print(sys.getsizeof(string))
"""


class Puzzle:
    def __init__(self, data : str | list | None):
        string = "000290307520107006000003020005800200802070060000002013450700130201500004379418650"
        self.grid = [[int(item) if item != "." else 0
                    for item in string[9*row:9*(row+1)]]
                    for row in range(9)]


    def find_Empty_Space(self) -> tuple | None:
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


    def dfs(self) -> bool:#Named after Depth First Search, basic backtracking algorithm
        pos = self.find_Empty_Space()#pos is given as a tuple (row, col)
        if pos == None:
            #Meaning the grid is full and solved
            return True

        row, col = pos

        for n in self.candidates[row][col]:

            if self.check(row, col, n):

                self.insert(row, col, n)

                if self.dfs():
                    #Causes all the recursion to unwind
                    return True

                self.insert(row, col, 0)

        return False
