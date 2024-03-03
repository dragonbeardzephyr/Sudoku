import kivy
import socket
import time
import random

from Generator.Generate import Puzzle
from Account import Account



# Function to pull base puzzles from file store,
# function to process base puzzles and form puzzles from them based on requirements of users. 

class Game:
    def __init__(self):

        self.modes = {"Classic": self.classic(),
                      "Multiplayer": self.multiplayer(),
                      "Account": self.account(),
                      "Best Times": self.bestTimes() }
        
        self.__account = Account()



    def load_Game_Data(self):
        with open("Game Data.txt", "r") as file:
            details = file.readlines


    def save_Game_Data(self, data):
        with open("Game Data.txt", "w") as file:
            file.write(data)


    def manage_Account(self):
        if not self.__account.loggedIn:
            #prompt user to register or log in
            self.__account.enter_Details()
            pass
        else:
            #prompt user if they would like to log out
            pass

    def classic(self):
        #Choose Difficulty
        #open corresponding puzzle file
        #Pull puzzle randomly from file
        #PLay the GaME
        #Finish
        pass

    def multiplayer(self):
        #Check if logged in, if not prompt to do so
        #otherwise connect to server
        #select how you want to match
        #play the game
        pass

    def best_Times(self):
        #Open best Times.txt
        #read data
        #sort to top 10 scores for each difficulty
        pass



    def select_Mode(self):
        pass


