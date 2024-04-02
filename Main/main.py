
"""from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout"""
import random
import os

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty

from kivy.config import Config
from pygame import CONTROLLERAXISMOTION

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

difficulties = ["easy", "normal", "hard", "extra_hard"]
class Game:
    def __init__(self):

        self.difficulty = "normal" # dafault
        self.puzzle = None
        self.puzzleSolution = None
        self.holding_Number = 0
        self.finishTime = 0
        self.timer = False
        
        self.opponentGrid = None

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
        self.client = None
        self.boot()


    def boot(self):
        self.load_Game_Data()
        if len(self.username) > 0 and len(self.password) > 0:
            self.client = Client()
            self.client.connect()
            if self.client.connected is True:
                if self.client.login(self.username, self.password, hashed = True):
                    self.online = True
                    self.client.update_BestTimes(self.topTimes)
                else:
                    print("Disconnected")
                    self.client.disconnect()
                    self.client = None

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


    def parse_Timer_to_String(self, timeFloat):
        minutes = str(int(timeFloat // 60))
        seconds = str(int(timeFloat % 60))
        return f"{'0'*(2-len(minutes))+minutes}:{'0'*(2-len(seconds))+seconds}"
    
        
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

#############################
#Cell Colours
NEUTRAL = (0, 1, 0.6, 1)
COLLISION = (1, 0, 0.5, 1)
CLUE = (0, 1, 0.6, 0.5)
TEXT = (0.76, 0, 1, 1)
#############################

class Cell(Button):
    def __init__(self, row, col, n, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.color = TEXT
        self.font_size = 20
        self.width = 10
        self.height = 10
        self.row = row
        self.col = col
        self.n = n

        if self.n > 0:
            self.text = str(n)
            self.disabled = True
            self.background_color = CLUE
        else:
            self.text = ""
            self.disabled = False
            self.background_color = NEUTRAL

        Clock.schedule_interval(self.checkCell, 1)

    def checkCell(self, dt):
        if not self.disabled and self.n != 0:#Dont need to waste time checking clue cells
            game.puzzle.insert(self.row, self.col, 0)#THis is so that it does not detect a collison with itself

            if game.puzzle.check(self.row, self.col, self.n) is False:
                self.background_color = COLLISION
            else:
                self.background_color = NEUTRAL

            game.puzzle.insert(self.row, self.col, self.n)

    def updateCell(self, n):
        self.n = n
        self.text = str(n)

        game.puzzle.insert(self.row, self.col, self.n)

        
    def clearCell(self):
        self.n = 0
        self.text = ""
        game.puzzle.insert(self.row, self.col, 0)
        self.background_color = NEUTRAL
        

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


class Timer(Label):
    def __init__(self, **kwargs):
        super(Timer, self).__init__(**kwargs)

class GameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

    def checks(self, dt):
        if game.timer:
            self.updateTimer()
        else:
            self.recentTime = time.time()

        game.win = game.puzzle.grid == game.puzzleSolution.grid
        if game.win:#check win
            print("Player WINS!")
            game.timer = False
            game.finishTime = self.saveTime

            topTime = app.topTimes[difficulties.index(game.difficulty)]
            topTime = float(topTime) if len(topTime) > 0 else 0

            if topTime == 0 or topTime > game.finishTime[0]:
                app.topTimes[difficulties.index(game.difficulty)] = str(game.finishTime[0])

            self.clock.cancel()
            game.win = False
            game.puzzle, game.puzzleSolution = None, None
            self.manager.current = "MainMenu"
        

    def updateTimer(self):
        self.elapsedTime += time.time() - self.recentTime
        self.recentTime = time.time()
        minutes = str(int(self.elapsedTime // 60))
        seconds = str(int(self.elapsedTime % 60))
        centiSeconds = str(int(round(self.elapsedTime % 60 - int(self.elapsedTime % 60), 2)*100))
        #print(f"{'0'*(2-len(minutes))+minutes}:{'0'*(2-len(seconds))+seconds}.{'0'*(2-len(centiSeconds))+centiSeconds}")
        self.ids.timer.text = f"{'0'*(2-len(minutes))+minutes}:{'0'*(2-len(seconds))+seconds}"
        self.saveTime = [round(self.elapsedTime, 2), self.ids.timer.text]

    def on_enter(self):
        self.set_Border()
        self.load()
        self.clock = Clock.schedule_interval(self.checks, 0.01)

    def load(self):
        game.import_Puzzle(game.difficulty)#assigns puzzle to game.puzzle
        game.puzzle.show_grid()
        grid = self.ids.grid

        i = 0
        j = 0
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box1.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 0
        j = 3
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box2.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 0
        j = 6
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box3.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 1
        j = 0
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box4.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 1
        j = 3
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box5.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 1
        j = 6
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box6.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 2
        j = 0
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box7.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 2
        j = 3
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box8.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 2
        j = 6
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box9.add_widget(Cell(x, y, game.puzzle.grid[x][y]))


        """
        for row in range(9):
            for col in range(9):
                grid.add_widget(Cell(row, col, game.puzzle.grid[row][col]))
        """

        numGrid = self.ids.numberGrid
        for n in range(1, 10):
            numGrid.add_widget(numberInput(n))

        self.recentTime = time.time()
        self.elapsedTime = 0
        game.timer = True

    def on_leave(self):
        self.ids.box1.clear_widgets()
        self.ids.box2.clear_widgets()
        self.ids.box3.clear_widgets()
        self.ids.box4.clear_widgets()
        self.ids.box5.clear_widgets()
        self.ids.box6.clear_widgets()
        self.ids.box7.clear_widgets()
        self.ids.box8.clear_widgets()
        self.ids.box9.clear_widgets()
        self.ids.numberGrid.clear_widgets()

    def pauseGame(self):
        pause = PauseScreen()
        pause.open()

class ClassicGame(GameScreen):
    pass


class OpponentGridCell(Button):
    def __init__(self, cellType, **kwargs):
        super(OpponentGridCell, self).__init__(**kwargs)
        self.width = 3
        self.height = 3
        self.text = ""
        if cellType == "1":
            self.background_color = (1, 1, 0, 1)
        else:
            self.background_color = NEUTRAL

    def updateCell(self, cellType):
        pass

class MultiplayerGame(GameScreen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

    def checks(self, dt):
        self.updateTimer()

        game.win = game.puzzle.grid == game.puzzleSolution.grid

        if game.win:#check win
            print("Player WINS!")
            game.timer = False
            game.finishTime = self.saveTime

            topTime = app.topTimes[difficulties.index(game.difficulty)]
            topTime = float(topTime) if len(topTime) > 0 else 0

            if topTime == 0 or topTime > game.finishTime[0]:
                app.topTimes[difficulties.index(game.difficulty)] = str(game.finishTime[0])

            self.clock.cancel()
            game.win = False
            game.puzzle, game.puzzleSolution, game.opponentGrid = None, None, None
            self.manager.current = "MainMenu"

        else:
            #recieve opppoenent grid
            if game.opponentGrid is not None:
                for i in range(81):
                    self.ids.opponentGrid.children[i].updateCell(game.opponentGrid[i])
        

    def updateTimer(self):
        self.elapsedTime += time.time() - self.recentTime
        self.recentTime = time.time()
        minutes = str(int(self.elapsedTime // 60))
        seconds = str(int(self.elapsedTime % 60))
        centiSeconds = str(int(round(self.elapsedTime % 60 - int(self.elapsedTime % 60), 2)*100))
        #print(f"{'0'*(2-len(minutes))+minutes}:{'0'*(2-len(seconds))+seconds}.{'0'*(2-len(centiSeconds))+centiSeconds}")
        self.ids.timer.text = f"{'0'*(2-len(minutes))+minutes}:{'0'*(2-len(seconds))+seconds}"
        self.saveTime = [round(self.elapsedTime, 2), self.ids.timer.text]

    def on_enter(self):
        self.set_Border()

        #RECEIVE GRID
        #initilaize stuff

        self.load()
        self.clock = Clock.schedule_interval(self.checks, 0.01)

    def load(self):#########Change this for multiplayer
        game.import_Puzzle(game.difficulty)#assigns puzzle to game.puzzle
        game.puzzle.show_grid()
        grid = self.ids.grid
        game.opponentGrid = "".join(str(random.sample((0, 1), 1)) for i in range(81)) # Will be revced by server as astring of 1s and 0s, 1s for cells that are complete and 0s for cells that arent

        i = 0
        j = 0
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box1.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 0
        j = 3
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box2.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 0
        j = 6
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box3.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 1
        j = 0
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box4.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 1
        j = 3
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box5.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 1
        j = 6
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box6.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 2
        j = 0
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box7.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 2
        j = 3
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box8.add_widget(Cell(x, y, game.puzzle.grid[x][y]))
        i = 2
        j = 6
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                self.ids.box9.add_widget(Cell(x, y, game.puzzle.grid[x][y]))


        numGrid = self.ids.numberGrid
        for n in range(1, 10):
            numGrid.add_widget(numberInput(n))

        opponentGrid = self.ids.opponentGrid

        for i in range(81):
            opponentGrid.add_widget(OpponentGridCell(game.opponentGrid[i]))

        self.recentTime = time.time()
        self.elapsedTime = 0
        game.timer = True

    def on_leave(self):
        self.ids.box1.clear_widgets()
        self.ids.box2.clear_widgets()
        self.ids.box3.clear_widgets()
        self.ids.box4.clear_widgets()
        self.ids.box5.clear_widgets()
        self.ids.box6.clear_widgets()
        self.ids.box7.clear_widgets()
        self.ids.box8.clear_widgets()
        self.ids.box9.clear_widgets()
        self.ids.numberGrid.clear_widgets()
        self.ids.opponentGrid.clear_widgets()


class PauseScreen(Popup):
    def on_open(self):
        game.timer = False

    def on_dismiss(self):
        game.timer = True

class ClassicMenu(Menu):
    def setDifficulty(self, difficulty):
        game.difficulty = difficulty




class MultiplayerMenu(Menu):
    def setDifficulty(self, difficulty):
        game.difficulty = difficulty




class AccountMenu(Menu):
    def clickLogout(self):
        if app.client and app.online is True:
            app.client.disconnect()
            app.client = None
            app.online = False
            self.set_Border()
            app.rememberLogin = False


class Login(BaseScreen):
    def togglePW(self):
        self.ids.password.password = not(self.ids.password.password)
    
    def toggleRememberLogin(self):
        app.rememberLogin = not(app.rememberLogin)

    def clickLogin(self):
        print("button clicked")
        un, pw = self.ids.username.text, self.ids.password.text
        print(un, pw)
        app.client = Client()
        app.client.connect()
 
        if app.client.connected:        
            if app.client.login(un, pw, hashed = False):
                app.online = True
                self.set_Border()

                if app.rememberLogin is True:
                    app.username = un
                    app.password = app.client.hashPW(pw)

                app.client.update_BestTimes(app.topTimes)
            
            else:
                app.client.disconnect()
                app.client = None
        else:
            app.client.disconnect()
            app.client = None
            print("COuld not connect to server")
                
    

class Register(BaseScreen):
    def clickRegister(self):
        print("Butoon Clicked")
        un , pw1, pw2 = self.ids.username.text, self.ids.password1.text, self.ids.password2.text
        if pw1 == pw2:
            app.client = Client()
            app.client.connect()
 
            if app.client.connected: 
                if app.client.register(un, pw1):
                    #register 
                    #display that registred
                    pass
                else:
                    #Use different username
                    pass
                    #error or usern
            else:
                app.client.disconnect()
                app.client = None
                print("Could not connect to server")
        else:
            app.client.disconnect()
            app.client = None
            print("Password do not match")

 
class BestTimes(BaseScreen):
    easy, normal, hard, extra_hard = "", "", "", ""
    def get_topTime(self, index):
        return app.topTimes[index]

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

