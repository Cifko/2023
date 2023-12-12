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
ogrid = Grid()
while data:
    next_line()
    if j == 0:
        grid.add_char_line("." * (len(line) + 2))
        ogrid.add_char_line("." * (len(line) + 2))
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    grid.add_char_line("." + line + ".")
    ogrid.add_char_line("." + line + ".")

grid.add_char_line("." * (len(line) + 2))
ogrid.add_char_line("." * (len(line) + 2))
x = y = 0
for i, line in enumerate(grid.grid):
    try:
        y = i
        x = line.index("S")
        break
    except:
        pass


def pos_move(from_pos, x0, y0, to_pos, x1, y1):
    delta_x = x1 - x0
    delta_y = y1 - y0
    if from_pos < to_pos:
        delta_x = -delta_x
        delta_y = -delta_y
        from_pos, to_pos = to_pos, from_pos
    if from_pos == "." or to_pos == ".":
        return False
    match (from_pos, to_pos):
        case ("F", "F"):
            return False
        case ("J", "J"):
            return False
        case ("7", "7"):
            return False
        case ("|", "-"):
            return False
        case ("L", "L"):
            return False
        case ("F", "-"):
            return delta_x == 1
        case ("-", "-"):
            return delta_x != 0
        case ("J", "-"):
            return delta_x == -1
        case ("J", "F"):
            return delta_x == -1 or delta_y == -1
        case ("F", "7"):
            return delta_x == 1
        case ("|", "F"):
            return delta_y == -1
        case ("|", "L"):
            return delta_y == 1
        case ("L", "J"):
            return delta_x == 1
        case ("J", "7"):
            return delta_y == -1
        case ("L", "7"):
            return delta_x == 1 or delta_y == -1
        case ("|", "7"):
            return delta_y == -1
        case ("L", "-"):
            return delta_x == 1
        case ("7", "-"):
            return delta_x == -1
        case ("|", "J"):
            return delta_y == 1
        case ("L", "F"):
            return delta_y == -1
        case ("|", "|"):
            return delta_y != 0
    print(from_pos, to_pos)
    exit()


visited = set()
next = [(x, y, 0)]
start_x = x
start_y = y
distance = defaultdict(lambda: math.inf)
if grid.grid[y][x - 1] == "-" and grid.grid[y][x + 1] == "-":
    ogrid.grid[y][x] = grid.grid[y][x] = "-"
elif grid.grid[y][x - 1] == "F" and grid.grid[y + 1][x] == "|":
    ogrid.grid[y][x] = grid.grid[y][x] = "7"
else:
    ogrid.grid[y][x] = grid.grid[y][x] = "F"
ogrid.grid[y][x] = grid.grid[y][x] = "|"
while next:
    x, y, moves = next.pop()
    if x < 0 or x >= len(grid.grid[0]) or y < 0 or y >= len(grid.grid):
        continue
    if moves < distance[(x, y)]:
        distance[(x, y)] = moves
    else:
        continue
    visited.add((x, y))
    match grid.grid[y][x]:
        case "|":
            if pos_move(grid.grid[y][x], x, y, grid.grid[y + 1][x], x, y + 1):
                next += [(x, y + 1, moves + 1)]
            if pos_move(grid.grid[y][x], x, y, grid.grid[y - 1][x], x, y - 1):
                next += [(x, y - 1, moves + 1)]
        case "-":
            if pos_move(grid.grid[y][x], x, y, grid.grid[y][x + 1], x + 1, y):
                next += [(x + 1, y, moves + 1)]
            if pos_move(grid.grid[y][x], x, y, grid.grid[y][x - 1], x - 1, y):
                next += [(x - 1, y, moves + 1)]
        case "L":
            if pos_move(grid.grid[y][x], x, y, grid.grid[y][x + 1], x + 1, y):
                next += [(x + 1, y, moves + 1)]
            if pos_move(grid.grid[y][x], x, y, grid.grid[y - 1][x], x, y - 1):
                next += [(x, y - 1, moves + 1)]
        case "7":
            if pos_move(grid.grid[y][x], x, y, grid.grid[y][x - 1], x - 1, y):
                next += [(x - 1, y, moves + 1)]
            if pos_move(grid.grid[y][x], x, y, grid.grid[y + 1][x], x, y + 1):
                next += [(x, y + 1, moves + 1)]
        case "J":
            if pos_move(grid.grid[y][x], x, y, grid.grid[y][x - 1], x - 1, y):
                next += [(x - 1, y, moves + 1)]
            if pos_move(grid.grid[y][x], x, y, grid.grid[y - 1][x], x, y - 1):
                next += [(x, y - 1, moves + 1)]
        case "F":
            if pos_move(grid.grid[y][x], x, y, grid.grid[y][x + 1], x + 1, y):
                next += [(x + 1, y, moves + 1)]
            if pos_move(grid.grid[y][x], x, y, grid.grid[y + 1][x], x, y + 1):
                next += [(x, y + 1, moves + 1)]

# s1 = 0
# for y in range(len(grid.grid)):
#     for x in range(len(grid.grid[0])):
#         if distance[(x, y)] == math.inf:
#             distance[(x, y)] = -1
#         print("%3s" % (distance[(x, y)]), end=" ")
#     print()
for x, y in distance.copy():
    if distance[(x, y)] > s1:
        c = 0
        match grid.grid[y][x]:
            case "F":
                if (
                    distance[(x + 1, y)] + 1 >= distance[(x, y)]
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y][x + 1], x + 1, y)
                    and distance[(x, y + 1)] + 1 == distance[(x, y)]
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y + 1][x], x, y + 1)
                ):
                    s1 = distance[(x, y)]
                    last = (x, y)
            case "J":
                if (
                    distance[(x - 1, y)] + 1 >= distance[(x, y)]
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y][x - 1], x - 1, y)
                    and distance[(x, y - 1)] + 1 == distance[(x, y)]
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y - 1][x], x, y - 1)
                ):
                    s1 = distance[(x, y)]
                    last = (x, y)
            case "L":
                if (
                    distance[(x + 1, y)] + 1 >= distance[(x, y)]
                    and distance[(x, y - 1)] + 1 == distance[(x, y)]
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y][x - 1], x - 1, y)
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y - 1][x], x, y - 1)
                ):
                    s1 = distance[(x, y)]
                    last = (x, y)
            case "7":
                if (
                    distance[(x - 1, y)] + 1 >= distance[(x, y)]
                    and distance[(x, y + 1)] + 1 == distance[(x, y)]
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y][x - 1], x - 1, y)
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y + 1][x], x, y + 1)
                ):
                    s1 = distance[(x, y)]
                    last = (x, y)
            case "-":
                if (
                    distance[(x - 1, y)] + 1 >= distance[(x, y)]
                    and distance[(x + 1, y)] + 1 == distance[(x, y)]
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y][x - 1], x - 1, y)
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y][x + 1], x + 1, y)
                ):
                    s1 = distance[(x, y)]
                    last = (x, y)
            case "|":
                if (
                    distance[(x, y - 1)] + 1 >= distance[(x, y)]
                    and distance[(x, y + 1)] + 1 == distance[(x, y)]
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y - 1][x], x, y - 1)
                    and pos_move(grid.grid[y][x], x, y, grid.grid[y + 1][x], x, y + 1)
                ):
                    s1 = distance[(x, y)]
                    last = (x, y)


cycle = set()


def fill(x, y, d):
    global cycle
    cycle.add((x, y))
    grid.grid[y][x] = "x"
    if d == 0:
        return
    if distance[(x + 1, y)] == d - 1:
        fill(x + 1, y, d - 1)
    if distance[(x - 1, y)] == d - 1:
        fill(x - 1, y, d - 1)
    if distance[(x, y + 1)] == d - 1:
        fill(x, y + 1, d - 1)
    if distance[(x, y - 1)] == d - 1:
        fill(x, y - 1, d - 1)


sys.setrecursionlimit(100000)
fill(last[0], last[1], s1)


def flood_fill(x, y):
    if grid.grid[y][x] == "x" or grid.grid[y][x] == "i":
        return 0
    next = [(x, y)]
    filled = 0
    while next:
        x, y = next.pop()
        if x < 0 or x >= len(grid.grid[0]) or y < 0 or y >= len(grid.grid):
            exit("Wrong side")
        if grid.grid[y][x] == "x" or grid.grid[y][x] == "i":
            continue
        filled += 1
        grid.grid[y][x] = "i"
        next += [(x + 1, y)]
        next += [(x - 1, y)]
        next += [(x, y + 1)]
        next += [(x, y - 1)]
    return filled


# for y, row in enumerate(grid.grid):
#     for x, cell in enumerate(row):
#         print("%3s(%d)" % (distance[(x, y)], (x, y) in cycle), end=" ")
#     print()
visited = set()
x, y = start_x, start_y
path = []
while True:
    path += [(x, y)]
    visited.add((x, y))
    if (
        (x + 1, y) in cycle
        and (x + 1, y) not in visited
        and distance[(x + 1, y)] == distance[(x, y)] + 1
        and pos_move(ogrid.grid[y][x], x, y, ogrid.grid[y][x + 1], x + 1, y)
    ):
        x = x + 1
    elif (
        (x - 1, y) in cycle
        and (x - 1, y) not in visited
        and distance[(x - 1, y)] == distance[(x, y)] + 1
        and pos_move(ogrid.grid[y][x], x, y, ogrid.grid[y][x - 1], x - 1, y)
    ):
        x = x - 1
    elif (
        (x, y - 1) in cycle
        and (x, y - 1) not in visited
        and distance[(x, y - 1)] == distance[(x, y)] + 1
        and pos_move(ogrid.grid[y][x], x, y, ogrid.grid[y - 1][x], x, y - 1)
    ):
        y = y - 1
    elif (
        (x, y + 1) in cycle
        and (x, y + 1) not in visited
        and distance[(x, y + 1)] == distance[(x, y)] + 1
        and pos_move(ogrid.grid[y][x], x, y, ogrid.grid[y + 1][x], x, y + 1)
    ):
        y = y + 1
    else:
        break

new_loop = True
while True:
    if not new_loop:
        path += [(x, y)]
        visited.add((x, y))
    new_loop = False
    if (x + 1, y) in cycle and (x + 1, y) not in visited and distance[(x + 1, y)] == distance[(x, y)] - 1:
        x = x + 1
    elif (x - 1, y) in cycle and (x - 1, y) not in visited and distance[(x - 1, y)] == distance[(x, y)] - 1:
        x = x - 1
    elif (x, y - 1) in cycle and (x, y - 1) not in visited and distance[(x, y - 1)] == distance[(x, y)] - 1:
        y = y - 1
    elif (x, y + 1) in cycle and (x, y + 1) not in visited and distance[(x, y + 1)] == distance[(x, y)] - 1:
        y = y + 1
    else:
        break
# if len(path) != s1 * 2:
#     print(path)
#     print(len(path), s1)
#     exit("Wrong path length")
# for y, row in enumerate(grid.grid):
#     for x, cell in enumerate(row):
#         print("%3s" % (distance[(x, y)]), end=" ")
#     print()
prev = None
x, y = path.pop(0)
while path:
    nx, ny = path.pop(0)
    side = -1
    if nx > x:
        s2 += flood_fill(x, y - side)
        s2 += flood_fill(nx, ny - side)
    if nx < x:
        s2 += flood_fill(x, y + side)
        s2 += flood_fill(nx, ny + side)
    if ny > y:
        s2 += flood_fill(x + side, y)
        s2 += flood_fill(nx + side, ny)
    if ny < y:
        s2 += flood_fill(x - side, y)
        s2 += flood_fill(nx - side, ny)
    x, y = nx, ny

print(grid)

# print(last, s1)
# print(grid)
# for y, row in enumerate(grid.grid):
#     for x, cell in enumerate(row):
#         if cell != "x":
#             s2 += flood_fill(x, y)
# # s2 = 0
# # for row in grid.grid:
# #     for cell in row:
# #         s2 += cell == " "
# print(grid)


if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    print("Part 1:", s1)
    pyperclip.copy(s1)  # type:ignore
# post_answer(day, 1, answer)
