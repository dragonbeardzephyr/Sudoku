from re import I
import time
import timeit
import cProfile
import random
import copy
import sys


def time_taken(func):
    st = time.perf_counter()
    func()
    et = time.perf_counter()
    print(et-st)



##print(sys.getsizeof(""))

#time_taken(lambda: print("Hello World!"))


for i in range(3):
    for j in (0, 3, 6):
        for x in range(3*i, 3*i+3):
            for y in range(j, j+3):
                print(f"{x},{y}")