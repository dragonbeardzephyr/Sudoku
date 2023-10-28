import pygame
import random
import time
import socket 

testGrid = [
    [3, 0, 0, 8, 0, 1, 0, 0, 2],
    [2, 0, 1, 0, 3, 0, 6, 0, 4],
    [0, 0, 0, 2, 0, 4, 0, 0, 0],
    [8, 0, 9, 0, 0, 0, 1, 0, 6],
    [0, 6, 0, 0, 0, 0, 0, 5, 0],
    [7, 0, 2, 0, 0, 0, 4, 0, 9],
    [0, 0, 0, 5, 0, 9, 0, 0, 0],
    [9, 0, 4, 0, 8, 0, 7, 0, 5],
    [6, 0, 0, 1, 0, 7, 0, 0, 3]
]

class puzzle:
    def __init__(self):
        self.__grid = [[0 for i in range(9)]for j in range(9)]
        self.__emptySpaces = []

    def show_grid(self):#for initial stages of development
        for i in self.__grid:
            for j in i:
                print(j, end = "  ")
            print()

    def generate(self):#Randomly generates a Sudoku puzzle with a unique Solution
        self.__grid = testGrid
        """   diffRange = {#Amount of given starting numbers based on difficulty
            1: (36, 40),#Easy
            2: (31, 35),#Medium
            3: (25, 30),#Hard
            4: (20, 24),#Extreme
            5: (17, 19)}#Evil
"""

    def validate(self):
        pass

    def get_Empty_Spaces(self):
        for y in range(9):
            for x in range(9):
                if self.__grid[y][x] == 0:
                    self.emptySpaces.append((y, x))


    def solve(self):
        

    def check_Move():
        pass

    def check_State():
        pass

