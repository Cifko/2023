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


last_line = None
s1 = s2 = x = 0
grid = Grid()
rules = {}
next_line()
rule = line
next_line()
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    game = explode(line, ["=", ","])
    rules[game[0][0]] = (game[1][0][1:], game[1][1][:-1])

position = "AAA"
i = 0
while position != "ZZZ":
    for r in rule:
        if r == "L":
            position = rules[position][0]
        else:
            position = rules[position][1]
        i += 1
s1 = i

starts = []
ends = []
s = set()
for node in rules:
    if node[-1] == "A":
        position = node
        i = 0
        while position[-1] != "Z":
            for r in rule:
                if r == "L":
                    position = rules[position][0]
                else:
                    position = rules[position][1]
                i += 1
        starts += [i]

g = 1
for s in starts:
    g = math.lcm(g, s)
s2 = g
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    print("Part 1:", s1)
    pyperclip.copy(s1)  # type:ignore
    # post_answer(day, 1, answer)
