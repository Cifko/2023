# type:ignore
from downloader import download, post_answer
from os.path import exists
from helper import *
import math
import sys
import re
import pyperclip
import time

# import pyperclip  # type:ignore
from collections import defaultdict

# pyperclip.copy("")  # type:ignore

day = int(sys.argv[0].split("/")[-1].split(".")[0])
file_name = f"{day:02}-input.txt"
download(day)
f = open(file_name)


def parse_value(x: str):
    try:
        return int(x)
    except:
        return x


def parse(line: str):
    # Try to parse line as a single value
    data = [parse_value(x) for x in line.split()]
    if len(data) == 1:
        data = data[0]
    # Try to parse line as a list of values
    nums = list(map(int, re.findall(r"(-?\d+)", line)))
    return (data, line, nums)


data = [parse(line.rstrip()) for line in f.readlines()]
a = line = nums = None
j = -1


def next_line():
    global data, a, line, nums, j
    a, line, nums = data.pop(0)
    j += 1


def explode(line: str, splitters: list[str] = []) -> list[Any]:
    if len(splitters) == 0:
        try:
            return int(line.strip())
        except:
            return line.strip()
    return list(map(lambda s: explode(s, splitters[1:]), line.strip().split(splitters[0])))


m = 0


def lagrange(x, xs, ys):
    global m
    res = 0
    for j in xs:
        s = 1
        k = 0
        for i in xs:
            s *= (x - i) if j != i else 1
            m = max(m, s if s > 0 else -s)
            while k < len(xs) and (j == k or s % (j - k) == 0):
                s //= j - k if j != k else 1
                k += 1
        s *= ys[j]
        res += s

    return res


last_line = None
s1 = s2 = x = 0
grid = Grid()
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    game = explode(line, ["=", ","])
    reps = [nums]
    s1 += lagrange(-1, list(range(len(nums))), nums)
    s2 += lagrange(len(nums), list(range(len(nums))), nums)
    # while nums.count(0) != len(nums):
    #     nums = list(map(lambda x: x[1] - x[0], zip(nums, nums[1:])))
    #     reps += [nums]
    # last = 0
    # first = 0
    # for i in range(len(reps) - 1):
    #     last = last + reps[-2 - i][-1]
    #     first = reps[-2 - i][0] - first
    # s1 += last
    # s2 += first
print(math.log2(m))
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
# else:
print("Part 1:", s1)
pyperclip.copy(s1)  # type:ignore
# post_answer(day, 1, answer)
