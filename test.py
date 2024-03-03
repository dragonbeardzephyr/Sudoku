import time
import timeit
import cProfile
import random
import copy
import sys


def time_taken(func = lambda x: x):
    st = time.time()
    func()
    et = time.time()
    print(et-st)



print(sys.getsizeof(""))

