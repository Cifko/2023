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
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    grid.add_row(map(int, line))


def solve(minc, maxc):
    m = [(0, 0, 0, 0, 0, 0, [])]
    vis = set()
    while m:
        s, x, y, c, dx, dy, p = heapq.heappop(m)
        key = (x, y, dx, dy, c)
        if key in vis:
            continue
        vis.add(key)
        if dx or dy:
            p.append((x, y))
            s += int(grid.cells[y][x])
        if x == len(grid.cells[0]) - 1 and y == len(grid.cells) - 1 and c >= minc:
            return s
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if dx == nx - x and dy == ny - y:
                if c == maxc:
                    continue
                nc = c + 1
            else:
                if c < minc and (dx or dy):
                    continue
                nc = 1
            if nx - x == -dx and ny - y == -dy:
                continue
            if nx < 0 or nx >= len(grid.cells[0]) or ny < 0 or ny >= len(grid.cells):
                continue
            heapq.heappush(m, (s, nx, ny, nc, nx - x, ny - y, list(p)))


s1 = solve(0, 3)
s2 = solve(4, 10)
print("Part 1:", s1)
pyperclip.copy(s1)  # type:ignore
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    pass
    # post_answer(day, 1, answer)
