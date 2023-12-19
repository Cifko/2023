# type:ignore
from downloader import download, post_answer
from os.path import exists
from helper import *
import sys
import re
import pyperclip  # type:ignore
from collections import defaultdict
from itertools import pairwise

sys.setrecursionlimit(100000)

pyperclip.copy("")  # type:ignore

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


s1 = s2 = 0
x1 = y1 = 0
x2 = y2 = 0
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    # grid.add_row(map(int, line))
    d1 = line[0]
    r1 = nums[0]
    d2 = "RDLU"[int(line[-2])]
    r2 = int(line[-7:-2], 16)
    match d1:
        case "L":
            x1 -= r1
            s1 += y1 * r1
        case "R":
            x1 += r1
            s1 -= y1 * r1
        case "D":
            y1 += r1
            s1 += x1 * r1
        case "U":
            y1 -= r1
            s1 -= x1 * r1
    s1 += r1
    match d2:
        case "L":
            x2 -= r2
            s2 += y2 * r2
        case "R":
            x2 += r2
            s2 -= y2 * r2
        case "D":
            y2 += r2
            s2 += x2 * r2
        case "U":
            y2 -= r2
            s2 -= x2 * r2
    s2 += r2
s1 = s1 // 2 + 1
s2 = s2 // 2 + 1
print("Part 1:", s1)
pyperclip.copy(s1)  # type:ignore
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    pass
    # post_answer(day, 1, answer)
