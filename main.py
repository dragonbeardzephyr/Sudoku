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
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


print("client start")
client_run()
print("client end")