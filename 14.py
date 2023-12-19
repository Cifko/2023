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
g = []
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    g += [list(line)]


def tilt(grid, dx, dy):
    for _ in range(len(g) * 2):
        for y in range(len(g)):
            for x in range(len(g[0])):
                if len(g) > y + dx >= 0 and len(g[0]) > x + dx >= 0 and g[y][x] == "O" and y > 0 and g[y + dy][x + dx] == ".":
                    g[y][x] = "."
                    g[y + dy][x + dx] = "O"


score = {}
rev_score = [0]
for mov in range(1000000000):
    for _ in range(len(g)):
        for y in range(len(g)):
            for x in range(len(g[0])):
                if g[y][x] == "O" and y > 0 and g[y - 1][x] == ".":
                    g[y][x] = "."
                    g[y - 1][x] = "O"
    if s1 == 0:
        for y, row in enumerate(g[::-1]):
            for c in row:
                if c == "O":
                    s1 += y + 1

    for _ in range(len(g)):
        for x in range(len(g[0])):
            for y in range(len(g)):
                if g[y][x] == "O" and x > 0 and g[y][x - 1] == ".":
                    g[y][x] = "."
                    g[y][x - 1] = "O"
    for _ in range(len(g)):
        for y in range(len(g))[::-1]:
            for x in range(len(g[0])):
                if g[y][x] == "O" and y + 1 < len(g) and g[y + 1][x] == ".":
                    g[y][x] = "."
                    g[y + 1][x] = "O"
    for _ in range(len(g)):
        for x in range(len(g[0]))[::-1]:
            for y in range(len(g)):
                if g[y][x] == "O" and x + 1 < len(g[0]) and g[y][x + 1] == ".":
                    g[y][x] = "."
                    g[y][x + 1] = "O"
    s = 0
    for y, row in enumerate(g[::-1]):
        for c in row:
            if c == "O":
                s += y + 1
    if (grid, s) in score:
        period = mov - score[(grid, s)]
        s2 = rev_score[mov - period + (10**9 - mov) % period]
        break
    score[(grid, s)] = mov
    rev_score += [s]

print("Part 1:", s1)
pyperclip.copy(s1)  # type:ignore
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    pass
    # post_answer(day, 1, answer)
