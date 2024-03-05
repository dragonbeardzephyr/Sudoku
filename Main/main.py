from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


import time
import random

from Generator.Generate import Puzzle
#from Account import Account


# Function to pull base puzzles from file store,
# function to process base puzzles and form puzzles from them based on requirements of users. 

class Game:
    def __init__(self):

        self.online = False
        self.rememberLogin = False

        self.load_Game_Data()


    def load_Game_Data(self):
        with open("Game Data.txt", "r") as file:
            details = file.readlines()

            self.username = details[0]
            self.password = details[1]
            self.topTimes = details[2:7]


    def save_Game_Data(self):
        with open("Game Data.txt", "w") as file:
            if self.rememberLogin:
                data = f"\n{self.username}\n{self.password}"
            else:
                data = "\n"

            data = "\n".join(self.topTimes)
            file.write(data)

    def import_Puzzle(self, difficulty):

        with open(f"Generator/{difficulty}.txt", "r") as file:
            puzzles = file.readlines()
            puzzle = Puzzle(random.choice(puzzles))
        
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


########################
########################
                    ####
                    ####
SudokuApp().run()   ####
                    ####
########################
########################
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