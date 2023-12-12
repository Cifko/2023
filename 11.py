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
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    if line.count("#") == 0:
        line = "e" * len(line)
    for i, c in enumerate(line):
        col_cnt[i] += c == "#"
    grid.add_char_line(line)

insert_to = []
for x in col_cnt:
    if col_cnt[x] == 0:
        insert_to.append(x)
insert_to.sort(reverse=True)
for y, row in enumerate(grid):
    for i in insert_to:
        grid.grid[y][i] = "e"

pos = []
for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == "#":
            pos.append((x, y))
# print(grid)
s1 = 0
# print(pos)
space = 1000000
for p in pos:
    for q in pos:
        if p >= q:
            continue
        dist = 0
        empty = 0
        for x in range(min(p[0], q[0]), max(p[0], q[0])):
            match grid[0][x]:
                case "e":
                    empty += 1
                case _:
                    dist += 1
        for y in range(min(p[1], q[1]), max(p[1], q[1])):
            match grid[y][0]:
                case "e":
                    empty += 1
                case _:
                    dist += 1
        s1 += dist + empty * 2
        s2 += dist + empty * space

print("Part 1:", s1)
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    pyperclip.copy(s1)  # type:ignore
# post_answer(day, 1, answer)
