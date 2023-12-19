# type:ignore
from downloader import download, post_answer
from os.path import exists
from helper import *
import sys
import re
import time
import pyperclip  # type:ignore
from collections import defaultdict

sys.setrecursionlimit(110 * 110 * 4)

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
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    grid.add_char_line(line)

m = 0


cache = defaultdict(set)


def cnt(x, y, dx, dy):
    if x < 0 or y < 0 or x >= len(grid.grid[0]) or y >= len(grid.grid):
        cache.clear()
    x += dx
    y += dy
    if x < 0 or y < 0 or x >= len(grid.grid[0]) or y >= len(grid.grid):
        return 0
    r = (x, y) not in cache
    if (dx, dy) in cache[(x, y)]:
        return 0
    cache[(x, y)].add((dx, dy))
    if grid.grid[y][x] == ".":
        r += cnt(x, y, dx, dy)
    elif grid.grid[y][x] == "/":
        r += cnt(x, y, -dy, -dx)
    elif grid.grid[y][x] == "\\":
        r += cnt(x, y, dy, dx)
    elif grid.grid[y][x] == "-":
        if dy != 0:
            r += cnt(x, y, dx - 1, 0)
            r += cnt(x, y, dx + 1, 0)
        else:
            r += cnt(x, y, dx, dy)
    elif grid.grid[y][x] == "|":
        if dx != 0:
            r += cnt(x, y, 0, dy - 1)
            r += cnt(x, y, 0, dy + 1)
        else:
            r += cnt(x, y, dx, dy)
    return r


s1 = cnt(-1, 0, 1, 0)
for ix in range(len(grid.grid[0])):
    s2 = max(s2, cnt(ix, -1, 0, 1))
    s2 = max(s2, cnt(ix, len(grid.grid), 0, -1))
for iy in range(len(grid.grid)):
    s2 = max(s2, cnt(-1, iy, 1, 0))
    s2 = max(s2, cnt(len(grid.grid[0]), iy, -1, 0))

print("Part 1:", s1)
pyperclip.copy(s1)  # type:ignore
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    pass
    # post_answer(day, 1, answer)
