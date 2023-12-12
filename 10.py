# type:ignore
from downloader import download, post_answer
from os.path import exists
from helper import *
import sys
import re
import pyperclip  # type:ignore

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

g = Grid()
while data:
    next_line()
    g.add_char_line(line)

g.add_border(".")

start_x, start_y = g.find_one("S")
left = g.grid[start_y][start_x - 1] in "-LF"
right = g.grid[start_y][start_x + 1] in "-J7"
up = g.grid[start_y - 1][start_x] in "|7F"
down = g.grid[start_y + 1][start_x] in "|JL"
if left:
    if up:
        g.grid[start_y][start_x] = "L"
    elif down:
        g.grid[start_y][start_x] = "7"
    else:
        g.grid[start_y][start_x] = "-"
elif right:
    if up:
        g.grid[start_y][start_x] = "J"
    elif down:
        g.grid[start_y][start_x] = "F"
elif up:
    if down:
        g.grid[start_y][start_x] = "|"


def upscale(cell: str):
    match cell:
        case ".":
            return ["   ", " . ", "   "]
        case "J":
            return [" x ", "xx ", "   "]
        case "L":
            return [" x ", " xx", "   "]
        case "7":
            return ["   ", "xx ", " x "]
        case "F":
            return ["   ", " xx", " x "]
        case "-":
            return ["   ", "xxx", "   "]
        case "|":
            return [" x ", " x ", " x "]
        case _:
            exit("Error: Upscaling")


g.upscale3x3(upscale)
# upscale start
x = start_x = start_x * 3 + 1
y = start_y = start_y * 3 + 1
prev_x = prev_y = None
path = set()
found = False
while not found:
    path.add((x, y))
    for next_x, next_y in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if g.grid[next_y][next_x] == "x" and (prev_x != next_x or prev_y != next_y):
            prev_x, prev_y = x, y
            x, y = next_x, next_y
            if x == start_x and y == start_y:
                found = True
            break
s2 = 0
for y in range(g.height):
    for x in range(g.width):
        if (x, y) in path:
            g.grid[y][x] = "x"
        else:
            g.grid[y][x] = " "
            s2 += 1
s1 = len(path) // 6
s2 -= g.flood_fill(0, 0, ".")
s2 = (s2 - len(path) + 8) // 9
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    print("Part 1:", s1)
    pyperclip.copy(s1)  # type:ignore
# post_answer(day, 1, answer)
