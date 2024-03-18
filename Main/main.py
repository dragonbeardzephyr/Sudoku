from kivy.app import App
"""from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout"""
from kivy.uix.screenmanager import ScreenManager, Screen
"""from kivy.uix.popup import Popup"""
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty

from kivy.config import Config

Config.set("graphics", "width", "1024")
Config.set("graphics", "height", "768")
Config.set("graphics", "reszizable", False)
Config.set('input', 'mouse', 'mouse,disable_multitouch')# Without this red dot appears at right click

"""
Inside box SIZE
1008, 713 within border
0.984, 0.928

return button
0.0078, 0.9375
"""

import time
import random

from Generator.Generate import Puzzle
from networking import Client

class Game:
    def __init__(self):

        self.difficulty = "normal" # dafault
        self.puzzle = None
        self.puzzleSolution = None
        self.holding_Number = 0


    def import_Puzzle(self, difficulty):

        with open(f"Main\Generator\{difficulty}.txt", "r") as file:
            puzzles = file.readlines()
            p = random.choice(puzzles)
            print(p)
            game.puzzle = Puzzle(p)
            game.puzzleSolution = Puzzle(p)
            game.puzzleSolution.solve()
            

########################
########################
game = Game()       ####
########################
########################

class SudokuApp(App):
    def __init__(self):
        super(SudokuApp, self).__init__()

        self.online = False
        self.rememberLogin = False
        self.client = Client()
        self.boot()


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
            if len(details) > 0:
                self.username = details[0].replace("\n", "")
                self.password = details[1].replace("\n", "")
                self.topTimes = [deets.replace("\n", "") for deets in details[2:7]]
            else:
                self.username = ""
                self.password = ""
                self.topTimes = ["", "", "", ""]

    def save_Game_Data(self):
        with open("Main\Game Data.txt", "w") as file:
            if self.rememberLogin is True:
                data = f"{self.username}\n{self.password}\n"
            else:
                data = ("\n\n")
            data += "\n".join(self.topTimes)
            file.write(data)


    def on_stop(self):
        self.save_Game_Data()
        print("Goodbye World")



class BaseScreen(Screen):
    borderFile = StringProperty("graphics\Sudoku_App_Border_Logged_Out.png")

    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)

    def on_enter(self):
        self.set_Border()

    def set_Border(self):
        if app.online is True: # Ignore red underline code works
            self.borderFile = "graphics\Sudoku_App_Border_Logged_In.png"
        else:
            self.borderFile = "graphics\Sudoku_App_Border_Logged_Out.png"
        
    
class MainMenu(BaseScreen):
    pass

class Menu(BaseScreen):
    pass


class Timer():
    pass

class Cell(Button):
    def __init__(self, row, col, n, **kwargs):
        super(Cell, self).__init__(**kwargs)

        self.neutral = (0, 1, 0.75, 0.75)
        self.collision = (1, 1, 0.75, 0.5)
        self.clue = (0, 1, 0.75, 1)

        self.width = 10
        self.height = 10
        self.row = row
        self.col = col
        self.n = n

        if self.n > 0:
            self.text = str(n)
            self.disabled = True
            self.background_color = self.clue
        else:
            self.text = ""
            self.disabled = False
            self.background_color = self.neutral

    def updateCell(self, n):
        self.n = n
        self.text = str(n)

        if game.puzzle.check(self.row, self.col, self.n) is False:
            self.background_color = self.collision
        else:
            self.background_color = self.neutral

        game.puzzle.insert(self.row, self.col, self.n)

        if game.puzzle.grid == game.puzzleSolution.grid:
            print("You Win")
        
    def clearCell(self):
        self.n = 0
        self.text = ""
        game.puzzle.insert(self.row, self.col, 0)
        self.background_color = self.neutral
        

    def on_press(self):
        if game.holding_Number > 0:
            self.updateCell(game.holding_Number)
            game.holding_Number = 0

        elif self.last_touch.button == "right":
            self.clearCell()
        
        
class numberInput(Button):
    def __init__(self, n, **kwargs):
        super(numberInput, self).__init__(**kwargs)
        self.width = 5
        self.height = 5
        self.n = n
        self.text = str(n)
        
    def on_press(self):
        game.holding_Number = self.n

class GameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

    def on_enter(self):
        self.load()

    def load(self):
        game.import_Puzzle(game.difficulty)#assigns puzzle to game.puzzle
        print(game.puzzle.grid)
        grid = self.ids.grid

        for row in range(9):
            for col in range(9):
                grid.add_widget(Cell(row, col, game.puzzle.grid[row][col]))

        numGrid = self.ids.numberGrid
        for n in range(1, 10):
            numGrid.add_widget(numberInput(n))

    def on_leave(self):
        self.ids.grid.clear_widgets()
        self.ids.numberGrid.clear_widgets()

    def pause(self):
        pass


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
    def clickLogout(self):
        if app.online is True:
            app.client.disconnect()
            app.online = False


class Login(BaseScreen):
    def togglePW(self):
        self.ids.password.password = not(self.ids.password.password)

    def clickLogin(self):
        print("button clicked")
        un, pw = self.ids.username.text, self.ids.password.text
        rememberLogin = True
        print(un, pw)
        
        if app.client.connect():
                
            if app.client.login(un, pw, hashed = False):
                app.online = True

                if rememberLogin is True:
                    app.username = un
                    app.password = app.client.hashPW(pw)
            else:
                pass
        else:
            print("COuld not connect to server")
                


class Register(BaseScreen):
    def clickRegister(self):
        print("Butoon CLicked")
        un , pw1, pw2 = self.ids.username.text, self.ids.password1.text, self.ids.password2.text
        if pw1 == pw2:
            if app.client.connect():
            
                if app.client.register(un, pw1):
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
app = SudokuApp()   ####
app.run()           ####
                    ####
########################
########################

