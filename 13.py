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


def equal(a, b):
    return a[::-1][: len(b)] == b[: len(a)]


def solve(grid, without=-1):
    pos = set(range(1, len(grid[0]))) - set([without])
    for row in grid:
        new_pos = set()
        for i in pos:
            if equal(row[:i], row[i:]):
                new_pos.add(i)
        pos = new_pos
        if not pos:
            return 0
    return pos.pop()


last_line = None
s1 = s2 = x = 0
col_cnt = defaultdict(int)
grid = []
while data:
    next_line()
    if line == "":
        hor = solve(grid)
        s1 += hor
        ver = solve(list(zip(*grid)))
        s1 += ver * 100
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                grid[y][x] = ".#"[cell == "."]
                s2 += solve(grid, hor) + solve(list(zip(*grid)), ver) * 100
                grid[y][x] = cell
        grid = []
    else:
        grid += [list(line)]
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
s2 //= 2
print("Part 1:", s1)
pyperclip.copy(s1)  # type:ignore
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    pass
    # post_answer(day, 1, answer)
