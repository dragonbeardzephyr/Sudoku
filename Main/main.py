from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup

from kivy.clock import Clock

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
        self.difficulty = "easy" # dafault


    def boot(self):
        self.load_Game_Data()
        if len(self.username) > 0 and len(self.password) > 0:
            self.client.connect()
            if self.client.connected is True:
                if self.client.login(self.username, self.password, hashed = True):
                    self.online = True
                else:
                    print("Disconnected")
                    self.client.disconnect()

            self.rememberLogin = True 


    def load_Game_Data(self):
        with open("Main\Game Data.txt", "r") as file:
            details = file.readlines()

            self.username = details[0].replace("\n", "")
            self.password = details[1].replace("\n", "")
            self.topTimes = [deets.replace("\n", "") for deets in details[2:7]]


    def save_Game_Data(self):
        with open("Main\Game Data.txt", "w") as file:
            if self.rememberLogin is True:
                data = f"{self.username}\n{self.password}\n"
            else:
                data = ("\n\n")
            data += "\n".join(self.topTimes)
            file.write(data)

    def import_Puzzle(self, difficulty):

        with open(f"Main\Generator\{difficulty}.txt", "r") as file:
            puzzles = file.readlines()
            puzzle = Puzzle(random.choice(puzzles))
            return puzzle


########################
########################
game = Game()       ####
########################
########################

class SudokuApp(App):
    def __init__(self):
        super(SudokuApp, self).__init__()
        game.boot()
        
    def on_stop(self):
        game.save_Game_Data()
        print("Goodbye World")

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.border = self.set_Border()

    def set_Border(self):
        if game.online: # Ignore red underline code works
            return "graphics\Sudoku_App_Border_Logged_In.png"
        else:
            return "graphics\Sudoku_App_Border_Logged_Out.png"

class MainMenu(BaseScreen):
    pass

class Menu(BaseScreen):
    pass


class Cell(Widget):
    def __init__(self, row, col, n, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.row = row
        self.col = col
        self.n = n

        if self.n > 0:
            self.text = str(n)
            self.disabled = True
        else:
            self.text = ""
            self.disabled = False

    def click(self):
        pass
        


class GameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

    def on_enter(self):
        self.load()

    def load(self):
        self.puzzle = game.import_Puzzle(game.difficulty)
        print(self.puzzle.grid)
        grid = self.ids.grid

        for row in range(9):
            for col in range(9):
                grid.add_widget(Cell(row, col, self.puzzle.grid[row][col]))

class ClassicMenu(Menu):
    def setDifficulty(self, difficulty):
        game.difficulty = difficulty

class ClassicGame(GameScreen):
    pass


class MultiplayerMenu(Menu):
    pass

class MultiplayerGame(GameScreen):
    pass

class AccountMenu(Menu):
    pass


class Login(BaseScreen):
    def togglePW(self):
        self.ids.password.password = not(self.ids.password.password)

    def clickLogin(self):
        print("button clicked")
        un, pw = self.ids.username.text, self.ids.password.text
        rememberLogin = True
        print(un, pw)
        
        if game.client.connect():
                
            if game.client.login(un, pw, hashed = False):
                game.online = True

                if rememberLogin is True:
                    game.username = un
                    game.password = game.client.hashPW(pw)
            else:
                pass
        else:
            print("COuld not connect to server")
                


class Register(BaseScreen):
    def clickRegister(self):
        print("Butoon CLicked")
        un , pw1, pw2 = self.ids.username.text, self.ids.password1.text, self.ids.password2.text
        if pw1 == pw2:
            if game.client.connect():
            
                if game.client.register(un, pw1):
                    #register 
                    #display that registred
                    pass
                else:
                    #Use different username
                    pass
                    #error or usern
            else:
                print("Could not connect to server")
        else:
            print("Password do not match")

 

class BestTimesMenu(Menu):
    pass

class BestTimes(BaseScreen):
    pass

class MainMenuManager(ScreenManager):
    pass



#############################

#############################


########################
########################
                    ####
SudokuApp().run()   ####
                    ####
########################
########################

