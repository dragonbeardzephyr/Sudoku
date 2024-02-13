import kivy
import socket
import time
import random

import Puzzle
import Main.Account as Account


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
            return file.readlines()

    def save_Game_Data(self, data):
        with open("Game Data.txt", "w") as file:
            file.write(data)


    def manage_Account(self):
        if not self.__account.loggedIn:
            #prompt user to register or log in
            pass
        else:
            #prompt user if they would like to log out
            pass

    def classic(self):
        #Choose Difficulty
        #With open corresponding puzzle file
        #Pull puzzle randomly from file
        #PLay the GaME
        #Finish
        pass

    def multiplayer(self):
        #Check if logged in, if not prompt to do so
        pass

    def best_Times(self):
        #Open best Times.txt
    
        pass



def play(mode):

    menu = {
        "Classic": classic(),
        "Multiplayer": multiplayer(),
        "Account": account(),
        "Best Times": bestTimes()
    }

    menu[mode]