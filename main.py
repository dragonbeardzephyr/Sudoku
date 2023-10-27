import pygame
import random
import time
import socket 


class puzzle:
    def __init__(self, difficulty):
        self.__grid = [[0 for i in range(9)]for j in range(9)]

    def show_grid(self):#for initial stages of development
        for i in self.__grid:
            for j in i:
                print(j, end = "  ")
            print()

    def generate(self):#Randomly generates a Sudoku puzzle with a unique Solution
        pass

    def validate(self):
        pass

    def solve(self):
        pass

    def checkMove():
        pass

    def checkState():
        pass


def client_run():
    