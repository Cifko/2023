# type:ignore
from time import time
import inspect
from helper import *
from random import randint
import heapq
import pyperclip


def measure_time(func):
    def inner(*args, **kwargs):
        is_method = inspect.getfullargspec(func).args[:1] == ["self"]
        start = time()
        res = func(*args, **kwargs)
        end = time()
        # print(
        #     f"Total time for {is_method and 'method' or 'func'} {is_method and args[0].__class__.__name__+'.' or ''}{func.__name__}({', '.join(list(map(str,args[is_method:]))+list(map(lambda x: f'{x} = {kwargs[x]}', kwargs)))}) is {end-start}"
        # )
        print(f"Total time for {is_method and 'method' or 'func'} {is_method and args[0].__class__.__name__+'.' or ''}{func.__name__} is {end-start}")
        return res

    return inner


# r = 1
# m = 0
# for i in range(32):
#     m += r
#     if m > 0:
#         m -= 1
#         r += 1
# print(m)
# print(20 * 20 * 8 * 40)
# a = MaxHeap()
# b = []
# for i in range(1000):
#     val = randint(0, 50)
#     a.push(val)
#     heapq.heappush(b, -val)

# while b:
#     if a.pop() != -heapq.heappop(b):
#         print("wtf")

# N = 100000
# arr = [randint(0, N // 3) for _ in range(N)]
# print(our_pop(our_push(arr)))
# print(our2_pop(our2_push(arr)))
# print(heapq_pop(heapq_push(arr)))
