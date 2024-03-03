import hashlib
import secrets
import random

class Account():
    def __init__(self):
        self.__username = ""   #3 < size < 15
        self.__password = ""   #7 < size
        self.__salt = ""
        self.loggedIn = False

    def register(self):
        #Open Connection
        #Send details to server 
        #Check that there are no existing record of same username
        #Insert username and hashed password as record
        #Send a Confirmation that the account has been registered
        #close connection
        pass

    def verify(self):#This will check with the Accounts database if username and password are correct, return true if so
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

        while not len(username) in range(5, 21):
            username = input()

        while not len(password) >= 7:
            password = input()

        #Convert password into hash

        self.__username = username
        self.__salt = random.sample(username+"QAZWSXEDCRFVTGBYHNUJMIKOLPthnyjmukiloprgbefvwdcqsxaz\/.,<>!£$%^&*()", 5)
        self.__password = hashedPassword = hashlib.sha256(password+salt)
        