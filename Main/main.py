import random
import threading

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
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
0.984, 0.928 ratio

return button
0.0078, 0.9375 ratio
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
        self.timerOn = False
        self.opponentGrid = None
        self.awaitingMatch = False

    def import_Puzzle(self, difficulty):

        with open(f"Main/Generator/{difficulty}.txt", "r") as file:
            puzzles = file.readlines()
            puzzle = random.choice(puzzles)
            print(puzzle)
            game.puzzle = Puzzle(puzzle)
            game.puzzleSolution = Puzzle(puzzle)
            game.puzzleSolution.solve()

    def parse_Timer_to_String(self, timeFloat):
        timeFloat =  float(timeFloat)
        hours = str(int(timeFloat // 3600))
        minutes = str(int(timeFloat % 3600 // 60))
        seconds = str(int(timeFloat % 60))
        #print(hours, minutes, seconds)
        #centiSeconds = str(int(round(self.elapsedTime % 60 - int(self.elapsedTime % 60), 2)*100))
        return ((f"{'0'*(2-len(hours))+hours}:" if int(hours) > 0 else "")
                +
                f"{'0'*(2-len(minutes))+minutes}:{'0'*(2-len(seconds))+seconds}")


########################
########################
game = Game()       ####
########################
########################

class SudokuApp(App):
    def __init__(self):
        super().__init__()

        self.online = False
        self.rememberLogin = False
        self.client = None
        self.boot()

        self.awaiting_Match = None



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

    def check_match_Found(self, dt):
        print("Chekcing math recieve found")
        matchFound = app.client.receive()
        print(matchFound)
        if matchFound == "Match Found":
            return True

        elif matchFound == "Match Not Found":
            return False



    def load_Game_Data(self):
        with open("Main/Game Data.txt", "r") as file:

            self.username = file.readline().replace("/n", "")
            self.password = file.readline().replace("/n", "")
            self.topTimes = [file.readline().replace("/n", "") for i in range(4)]

            print(self.username)
            print(self.password)
            print(self.topTimes)


    def save_Game_Data(self):
        with open("Main/Game Data.txt", "w") as file:
            if self.rememberLogin is True:
                data = f"{self.username}/n{self.password}/n"
            else:
                data = ("/n/n")
            data += "/n".join([time if len(time) > 0 else "/n" for time in self.topTimes])
            file.write(data)

    def on_stop(self):
        self.save_Game_Data()
        print("Goodbye World")

class MenuManager(ScreenManager):
    pass

class BaseScreen(Screen):
    borderFile = StringProperty("graphics/Sudoku_App_Border_Logged_Out.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.set_Border()

    def set_Border(self):
        if app.online is True: # Ignore red underline code works
            self.borderFile = "graphics/Sudoku_App_Border_Logged_In.png"
        else:
            self.borderFile = "graphics/Sudoku_App_Border_Logged_Out.png"


class MainMenu(BaseScreen):
    pass

class Menu(BaseScreen):
    pass


class ClassicMenu(Menu):
    def setDifficulty(self, difficulty):
        game.difficulty = difficulty



class MultiplayerMenu(Menu):
    def setDifficulty(self, difficulty):
        game.difficulty = difficulty

    def match(self):
        if app.client and app.online is True:
            print("About to match")
            if app.client.match_Players(game.difficulty):
                print("matching good")
                self.ids.returnButton.disabled = True


                game.awaitingMatch = True
                matchingPopup = Popup(title = "Matching", content = Label(text = "Waiting for opponent"), size_hint = (0.7, 0.7))
                matchFound = Clock.schedule_once(app.check_match_Found, 0.1)
                matchingPopup.open()

                if matchFound:
                    self.ids.returnButton.disabled = False
                    self.manager.current = "MultiplayerGame"

                else:
                    p = Popup(title = "Unsuccessful", content = Label(text = "No match found, retry"), size_hint = (0.6, 0.6))
                    p.open()
                    self.ids.returnButton.disabled = False
                    print("Matching not good")



            else:
                print("Matching not good")
        else:
            popup = Popup(title = "Error", content = Label(text = "You need to login"), size_hint = (0.5, 0.5))
            popup.open()



class AccountMenu(Menu):
    def get_Username(self):
        return app.username

    def clickLogout(self):
        if app.client and app.online is True:
            app.client.disconnect()
            app.client = None
            app.online = False
            self.set_Border()
            app.rememberLogin = False




#############################
#Cell Colours
NEUTRAL = (0, 1, 0.6, 1)
COLLISION = (1, 0, 0.5, 1)
#CLUE = (0, 1, 0.6, 1)
TEXT = (0.76, 0, 1, 1)
#############################

class Cell(Button):
    def __init__(self, row, col, n, **kwargs):
        super().__init__(**kwargs)
        self.color = TEXT
        self.font_size = 20
        self.width = 10
        self.height = 10
        self.row = row
        self.col = col
        self.n = n
        self.background_color = NEUTRAL

        if self.n > 0:
            self.text = str(n)
            self.disabled = True

        else:
            self.text = ""
            self.disabled = False


        self.clock = Clock.schedule_interval(self.checkCell, 0.5)

    def checkCell(self, dt):
        if self.n != 0:
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


class NumberInput(Button):
    def __init__(self, n, **kwargs):
        super().__init__(**kwargs)
        self.width = 5
        self.height = 5
        self.n = n
        self.text = str(n)

    def on_press(self):
        game.holding_Number = self.n


class Timer(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class GameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            numGrid.add_widget(NumberInput(n))

        self.recentTime = time.time()
        self.elapsedTime = 0
        game.timerOn = True


    def checks(self, dt):
        if game.timerOn:
            self.updateTimer()
        else:
            self.recentTime = time.time()

        game.win = game.puzzle.grid == game.puzzleSolution.grid
        if game.win:#check win
            print("Player WINS!")
            self.clock.cancel()
            game.timerOn = False
            game.finishTime = self.saveTime

            topTime = app.topTimes[difficulties.index(game.difficulty)]
            topTime = float(topTime) if len(topTime) > 0 else 0

            newRecord = False
            if topTime == 0 or topTime > game.finishTime[0]:
                newRecord = True
                app.topTimes[difficulties.index(game.difficulty)] = str(game.finishTime[0])

            game.win = False

            p = Popup(title = "Congratulations",
                content = Label(text = f"{'New record!/n' if newRecord else ''}Complete Time: {game.finishTime[1]}"),
                size_hint = (0.6, 0.3))
            p.open()

            self.manager.current = "MainMenu"


    def updateTimer(self):
        self.elapsedTime += time.time() - self.recentTime
        self.recentTime = time.time()

        self.ids.timer.text = game.parse_Timer_to_String(self.elapsedTime)
        self.saveTime = [round(self.elapsedTime, 2), self.ids.timer.text]



    def on_leave(self):
        self.clock.cancel()

        for i in self.ids.box1.children:
            i.clock.cancel()
        for i in self.ids.box2.children:
            i.clock.cancel()
        for i in self.ids.box3.children:
            i.clock.cancel()
        for i in self.ids.box4.children:
            i.clock.cancel()
        for i in self.ids.box5.children:
            i.clock.cancel()
        for i in self.ids.box6.children:
            i.clock.cancel()
        for i in self.ids.box7.children:
            i.clock.cancel()
        for i in self.ids.box8.children:
            i.clock.cancel()
        for i in self.ids.box9.children:
            i.clock.cancel()

        game.puzzle, game.puzzleSolution = None, None

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


class ClassicGame(GameScreen):
    def pauseGame(self):
        pause = PauseScreen()
        pause.open()


class OpponentGridCell(Button):
    def __init__(self, cellType, **kwargs):
        super().__init__(**kwargs)
        self.width = 3
        self.height = 3
        self.text = ""
        if cellType == "1":
            self.background_color = (1, 1, 0, 1)
        else:
            self.background_color = NEUTRAL

    def updateCell(self, cellType):
        if cellType == "1":
            self.background_color = (1, 1, 0, 1)
        else:
            self.background_color = NEUTRAL



class MultiplayerGame(GameScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def checks(self, dt):

        #GET OPPONENT GRID SOMEHOW
        app.client.send(game.puzzle.grid_To_String())

        game.opponentGrid = app.client.receive()

        if game.opponentGrid == "LOSE":
            print("Opponent Wins!")
            self.clock.cancel()
            game.timerOn = False

            p = Popup(title = "Unlucky", content = Label(text = "Opponent Wins!"), size_hint = (0.4, 0.35))
            p.open()
            self.manager.current = "MainMenu"

        elif game.opponentGrid is not None:
            for i in range(81):
                self.ids.opponentGrid.children[80-i].updateCell(game.opponentGrid[i])

        print(game.opponentGrid)

        if game.timerOn:
            self.updateTimer()
        else:
            self.recentTime = time.time()

        game.win = game.puzzle.grid == game.puzzleSolution.grid

        if game.win:#check win
            app.client.send("WIN")

            self.clock.cancel()
            print("Player WINS!")
            game.timerOn = False
            game.finishTime = self.saveTime
            game.win = False

            topTime = app.topTimes[difficulties.index(game.difficulty)]
            topTime = float(topTime) if len(topTime) > 0 else 0

            newRecord = False
            if topTime == 0 or topTime > game.finishTime[0]:
                newRecord = True
                app.topTimes[difficulties.index(game.difficulty)] = str(game.finishTime[0])


            p = Popup(title = "Congratulations",
                    content = Label(text = f"{'New record!/n' if newRecord else ''}You Win/nComplete Time: {game.finishTime[1]}"),
                    size_hint = (0.6, 0.3))

            p.open()

            self.manager.current = "MainMenu"
            print("Exit")



    def updateTimer(self):
        self.elapsedTime += time.time() - self.recentTime
        self.recentTime = time.time()

        self.ids.timer.text = game.parse_Timer_to_String(self.elapsedTime)
        self.saveTime = [round(self.elapsedTime, 2), self.ids.timer.text]

    def on_enter(self):
        self.set_Border()

        #RECEIVE GRID
        #initilaize stuff
        self.load()
        self.clock = Clock.schedule_interval(self.checks, 0.01)

    def load(self):#########Change this for multiplayer

        puzzleString = app.client.receive()

        game.puzzle = Puzzle(puzzleString)
        game.puzzleSolution = Puzzle(puzzleString)
        game.puzzleSolution.solve()

        grid = self.ids.grid
        game.opponentGrid = "".join([str(0) for i in range(81)]) # Will be revced by server as astring of 1s and 0s, 1s for cells that are complete and 0s for cells that arent

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
            numGrid.add_widget(NumberInput(n))

        opponentGrid = self.ids.opponentGrid
        for i in range(81):
            opponentGrid.add_widget(OpponentGridCell(game.opponentGrid[i]))

        self.recentTime = time.time()
        self.elapsedTime = 0
        game.timerOn = True

    def on_leave(self):
        self.clock.cancel()
        for i in self.ids.box1.children:
            i.clock.cancel()
        for i in self.ids.box2.children:
            i.clock.cancel()
        for i in self.ids.box3.children:
            i.clock.cancel()
        for i in self.ids.box4.children:
            i.clock.cancel()
        for i in self.ids.box5.children:
            i.clock.cancel()
        for i in self.ids.box6.children:
            i.clock.cancel()
        for i in self.ids.box7.children:
            i.clock.cancel()
        for i in self.ids.box8.children:
            i.clock.cancel()
        for i in self.ids.box9.children:
            i.clock.cancel()

        game.puzzle, game.puzzleSolution, game.opponentGrid = None, None, None

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


    def pauseGame(self):
        pass

class PauseScreen(Popup):
    def on_open(self):
        game.timerOn = False

    def on_dismiss(self):
        game.timerOn = True


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
                    app.save_Game_Data()

                app.client.update_BestTimes(app.topTimes)

            else:
                app.client.disconnect()
                app.client = None
                p = Popup(title = "Error", content = Label(text = "Invalid Username or Password"), size_hint = (0.6, 0.3))
                p.open()

        else:
            app.client.disconnect()
            app.client = None
            p  = Popup(title = "Error", content = Label(text = "Could not connect to server, try again otherwise server must be offline"), size_hint = (0.6, 0.3))
            p.open()


class Register(BaseScreen):
    def clickRegister(self):
        print("Butoon Clicked")
        un , pw1, pw2 = self.ids.username.text, self.ids.password1.text, self.ids.password2.text

        if len(pw1) < 7 or len(pw2) < 7:
            p = Popup(title = "Error", content = Label(text = "Password must be at least 7 characters long"), size_hint = (0.6, 0.3))
            p.open()
            return

        if pw1 != pw2:
            p = Popup(title = "Error", content = Label(text = "Passwords do not match"), size_hint = (0.6, 0.3))
            p.open()
            return

        app.client = Client()
        app.client.connect()

        if app.client.connected:
            if app.client.register(un, pw1):
                loggedIn = app.client.login(un, pw1, False)

                p = Popup(title = "Success", content = Label(text = "Account has been created" + "/nAnd you have been logged in" if loggedIn else ""), size_hint = (0.6, 0.3))
                p.open()


            else:
                p = Popup(title = "Error", content = Label(text = "Username already taken"), size_hint = (0.6, 0.3))
                p.open()
        else:
            app.client.disconnect()
            app.client = None
            p = Popup(title = "Error", content = Label(text = "Could not connect to server"), size_hint = (0.6, 0.3))
            p.open()




class BestTimes(BaseScreen):
    def on_enter(self):
        self.ids.easyTime.text = self.get_Top_Time(0)
        self.ids.normalTime.text = self.get_Top_Time(1)
        self.ids.hardTime.text = self.get_Top_Time(2)
        self.ids.extraHardTime.text = self.get_Top_Time(3)

    def get_Top_Time(self, index):
        topTime = app.topTimes[index]
        return game.parse_Timer_to_String(topTime) if len(topTime) > 0 else "N/A"




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

