# type:ignore
from downloader import download, post_answer
from os.path import exists
from helper import *
import sys
import re
import pyperclip  # type:ignore
from collections import defaultdict

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


answer = None
s = x = 0

last_line = None
s1 = s2 = x = 0
grid = Grid()
col_cnt = defaultdict(int)
boxs = defaultdict(list)
box_map = defaultdict(int)
lens = defaultdict(int)
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    parts = line.split(",")
    for a in parts:
        c = 0
        for x in a:
            c += ord(x)
            c *= 17
            c %= 256
        c = 0
        b = ""
        for x in a:
            if x == "=":
                if b not in box_map:
                    box_map[b] = c
                    boxs[c] += [b]
                lens[b] = int(a.split("=")[1])
            if x == "-":
                if b in boxs[box_map[b]]:
                    boxs[box_map[b]].remove(b)
                del box_map[b]
            b += x
            c += ord(x)
            c *= 17
            c %= 256
        s1 += c
    # print(boxs)
    for box in sorted(boxs):
        for i, b in enumerate(boxs[box]):
            s2 += (box + 1) * (i + 1) * lens[b]

print("Part 1:", s1)
pyperclip.copy(s1)  # type:ignore
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    pass
    # post_answer(day, 1, answer)
