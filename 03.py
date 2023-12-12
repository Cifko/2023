# type:ignore
from downloader import download, post_answer
from os.path import exists
from helper import *
import sys
import re
import pyperclip  # type:ignore
from collections import defaultdict

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


def explode(line: str, splitters: list[str] = []) -> list[Any]:
    if len(splitters) == 0:
        return line.strip()
    return list(map(lambda s: explode(s, splitters[1:]), line.strip().split(splitters[0])))


answer = last_line = None
s1 = s2 = x = 0
grid = Grid()
all_nums = []
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    # if j <= 10:
    # print(j, a)
    game = explode(line, [":", ";", ",", " "])
    grid.add_char_line(line)
    all_nums.extend(nums)
    s1 += 0
    s2 += 0

n = ""
graph = defaultdict(list)
for y in range(grid.height):
    is_number = False
    for x in range(grid.width):
        if grid[y][x] in "0123456789":
            if not is_number:
                end = start = x
                while end < grid.width and grid[y][end] in "0123456789":
                    end += 1
                num = int("".join(grid[y][start:end]))
                symbol = 0
                for xx in range(start - 1, end + 1):
                    if grid.width > xx >= 0:
                        for yy in range(y - 1, y + 2):
                            if grid.height > yy >= 0:
                                if grid[yy][xx] not in "0123456789.":
                                    graph[(xx, yy)].append(num)
                                    symbol += 1
                if symbol > 0:
                    if symbol > 1:
                        print("ERROR")
                    s1 += num
            is_number = True
        else:
            is_number = False

for (x, y), nums in graph.items():
    if len(nums) == 2:
        if grid[y][x] == "*":
            s2 += nums[0] * nums[1]
if s2:
    print(s2)
    pyperclip.copy(s2)  # type:ignore
else:
    print(s1)
    pyperclip.copy(s1)  # type:ignore

if answer is not None:
    post_answer(day, 1, answer)
