from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image


import time
import random

from Generator.Generate import Puzzle
from networking import Client


# Function to pull base puzzles from file store,
# function to process base puzzles and form puzzles from them based on requirements of users. 

class Game:
    def __init__(self):

        self.online = False
        self.rememberLogin = False
        self.boot()
        self.load_Game_Data()

    def boot(self):
        self.load_Game_Data()
        if len(self.username) > 0 and len(self.password) > 0:
            pass
            #do some login stuff

        else:
            pass

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

class PauseScreen(Widget):
    pass

class ClassicMenu(Screen):
    pass

class ClassicGame(Screen):
    pass

class ClassicPause(PauseScreen):
    pass

class MultiplayerMenu(Screen):
    pass

class MultiplayerGame(Screen):
    pass

class MultiplayerPause(PauseScreen):
    pass

class AccountMenu(Screen):
    pass

class Login(Screen):
    pass

class Register(Screen):
    pass

class BestTimesMenu(Screen):
    pass

class BestTimes(Screen):
    pass

class MainMenuManager(ScreenManager):
    pass








########################
########################
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