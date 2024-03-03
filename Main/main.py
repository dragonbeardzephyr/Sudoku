from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


import sys
sys.path.append("../Sudoku_Code")
import time
import random


#from Account import Account


# Function to pull base puzzles from file store,
# function to process base puzzles and form puzzles from them based on requirements of users. 

class Game:
    def __init__(self):

        
        self.modes = {"Classic": self.classic(),
                      "Multiplayer": self.multiplayer(),
                      "Account": self.manage_Account(),
                      "Best Times": self.best_Times() }
        
        #self.__account = Account()



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

    def import_Puzzle(self, difficulty):
        pass

    def select_Mode(self):
        pass


 
class SudokuApp(App):
    pass

class MainMenu(Screen):
    pass

class ClassicMenu(Screen):
    pass

class MultiplayerMenu(Screen):
    pass

class AccountMenu(Screen):
    pass

class BestTimesMenu(Screen):
    pass

class MainMenuManager(ScreenManager):
    pass

SudokuApp().run()

"""
MainMenu
    AccountMenu

    ModeSelectScreen
        ClassicSudokuDifficultySelect

        MultiplayerModeSelect#match + Difficulty

        BestTimesDifficultySelect

GameScreen
    ClassicGameScreen

    MultiplayerGameScreen


PauseScreen
    ClassicPauseScreen

    MultiplayerPauseScreen


AccountScreen
    RegisterScreen

    LoginScreen


BestTimesScreen




"""