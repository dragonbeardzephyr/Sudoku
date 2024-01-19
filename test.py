import time


def time_taken(func = lambda x: x):
    st = time.time()
    func()
    et = time.time()
    print(et-st)

def fart(x):
    print("frpppp")

def nothing():
    return 

time_taken(fart)