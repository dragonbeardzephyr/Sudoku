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



##print(sys.getsizeof(""))

start = time.time()
time.sleep(3.5)
time = time.time() - start
minutes = str(int(time // 60))
seconds = str(int(time % 60))
centiSeconds = str(int(round(time % 60 - int(time % 60), 2)*100))
print(f"{'0'*(2-len(minutes))+minutes}:{'0'*(2-len(seconds))+seconds}.{centiSeconds}")