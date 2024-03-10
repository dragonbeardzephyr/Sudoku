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
from networking import Client


# Function to pull base puzzles from file store,
# function to process base puzzles and form puzzles from them based on requirements of users. 

class Game:
    def __init__(self):

        self.online = False
        self.rememberLogin = False
        self.client = Client()
        self.boot()


    def boot(self):
        self.load_Game_Data()
        if len(self.username) > 0 and len(self.password) > 0:
            self.client.connect()
            if self.client.connected:
                if self.client.login(self.username, self.password):
                    self.online = True
                    self.rememberLogin = True


    def load_Game_Data(self):
        with open("Main\Game Data.txt", "r") as file:
            details = file.readlines()

            self.username = details[0].strip("\n")
            self.password = details[1].strip("\n")
            self.topTimes = [deets.strip("\n") for deets in details[2:7]]


    def save_Game_Data(self):
        with open("Game Data.txt", "w") as file:
            if self.rememberLogin:
                data = f"\n{self.username}\n{self.password}"
            else:
                data = "\n\n"

            data = "\n".join(self.topTimes)
            file.write(data)

    def import_Puzzle(self, difficulty):

        with open(f"Generator/{difficulty}.txt", "r") as file:
            puzzles = file.readlines()
            puzzle = Puzzle(random.choice(puzzles))
            return puzzle


class SudokuApp(App, Game):
    def __init__(self):
        super(SudokuApp, self).__init__()
        self.game = Game()

    def on_stop(self):
        self.game.save_Game_Data()
        print("Goodbye World")

class BaseScreen(Screen):
    def set_Border(self):
        app = SudokuApp.get_running_app()
        if app.game.online: # Ignore red underline code works
            return "graphics\Sudoku_App_Border_Logged_In.png"
        else:
            return "graphics\Sudoku_App_Border_Logged_Out.png"


class MainMenu(BaseScreen):
    pass

class Menu(BaseScreen):
    pass

class GameScreen(BaseScreen):
    pass

class ClassicMenu(Menu):
    pass

class ClassicGame(GameScreen):
    pass


class MultiplayerMenu(Menu):
    pass

class MultiplayerGame(GameScreen):
    pass

class AccountMenu(Menu):
    pass

class Login(BaseScreen):
    pass

class Register(BaseScreen):
    pass

class BestTimesMenu(Menu):
    pass

class BestTimes(BaseScreen):
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

