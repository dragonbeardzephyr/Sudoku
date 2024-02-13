import time
import timeit
import cProfile

def time_taken(func = lambda x: x):
    st = time.time()
    func()
    et = time.time()
    print(et-st)




cProfile.run("")
#timeit.timeit("")



