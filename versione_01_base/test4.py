import math
import multiprocessing
from multiprocessing import Array
from multiprocessing import Value
from multiprocessing.shared_memory import SharedMemory
from numba import jit, njit
import numpy as np

import os
os.system('clear')






# @jit
def process2b(a,v):
    a[1] += 0.19
    v.value = 23.37
    return a,v



def test4(ist):
    print(ist.name)

    a = ist.shared_array
    v = ist.shared_value



    print(a[1],v)
    p2 = multiprocessing.Process(target=process2b, args=(a,v))

    p2.start()
    p2.join()

    v1 = v.value
    # v = q.get()
    # print(v)

    print(a[1],v1)
    print("--end--")


class myProgram:
    def __init__(self, name):
        self.name = name
        self.shared_array = Array('d',[1,2,3,4,5])
        # Creazione di un Value condiviso
        self.shared_value = Value('d', 10)  # Un singolo intero inizializzato a 10

        test4(self)

    def run(self):
        self.display_info()
    def display_info(self):
         print(f'questa è una istanza del programma: {self.name}')



# # @jit
# def process2a(q,a):
#       v = q.get()
#       print(a[1],v)
#       v += 1
#       q.put(v)

if __name__ == "__main__":
    program = myProgram('esempio nome del programma')
    program.run()