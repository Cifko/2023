# type:ignore
from downloader import download, post_answer
from os.path import exists
from helper import *
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
        return line.strip()
    return list(map(lambda s: explode(s, splitters[1:]), line.strip().split(splitters[0])))


last_line = None
s1 = s2 = x = 0
grid = Grid()
all_nums = []
won = []
cards = []
seeds = None
name = None
d = defaultdict(list)
next_line()
times = nums
next_line()
distances = nums
s1 = 1
for time, dist in zip(times, distances):
    s = 0
    for i in range(1, time):
        distance = (time - i) * i
        if distance > dist:
            s += 1
    s1 *= s
times = [int("".join(map(str, times)))]
distances = [int("".join(map(str, distances)))]
s2 = 1
for time, dist in zip(times, distances):
    s = 0
    for i in range(1, time):
        distance = (time - i) * i
        if distance > dist:
            s += 1
    s2 *= s
# while data:
#     next_line()
#     # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
#     # if j <= 10:
#     # print(j, a)
#     game = explode(line, [":", "|"])

if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    print("Part 1:", s1)
    pyperclip.copy(s1)  # type:ignore
    # post_answer(day, 1, answer)
