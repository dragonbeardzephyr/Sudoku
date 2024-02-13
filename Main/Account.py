import hashlib
import secrets

class Account():
    def __init__(self):
        self.__username = ""   """3 < size < 15"""
        self.__password = ""   """7 < size"""
        self.loggedIn = False

    def register(self):
        #Open Connection
        #Send details to server 
        #Check that there are no existing record of same username
        #Insert username and hashed password as record
        #Send a Confirmation that the account has been registered
        #close connection
        pass

    def verify(self):#This will check if username and password are correct, return true if so
        pass

    def login(self):
        #Open connection
        #Send detaisl to server
        #Server will check username and passwrod
        #if they match good
        #Server will send a confirmation that the login was good, and will update user to the online list
        #logedIN variable will be set to true
        #Close Connection

        if self.verify() == True:
            self.loggedIn = True
            
        else:
            print("Login Unsuccessful")



    def enter_Details(self):
        username = ""
        password = ""

        while len(username) in range(3, 6):
            username = input()

        while len(password) >= 7:
            password = input()

        #Convert password into hash



