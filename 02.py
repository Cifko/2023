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
        try:
            return int(line.strip())
        except:
            return line.strip()
    return list(map(lambda s: explode(s, splitters[1:]), line.strip().split(splitters[0])))


answer = None
s1 = s2 = x = 0
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    # if j <= 10:
    #     print(j, a)
    id, rest = line.split(":")
    game = explode(line, [":", ";", ",", " "])
    maxs = defaultdict(int)
    possible = True
    for row in game[1]:
        for a, c in row:
            maxs[c] = max(maxs[c], a)
    s2 += maxs["red"] * maxs["green"] * maxs["blue"]
    if maxs["red"] > 12 or maxs["green"] > 13 or maxs["blue"] > 14:
        possible = False

    # maxs = defaultdict(int)
    # for game in rest.split(";"):
    #     cubes = game.split(",")
    #     cc = {}
    #     colors = defaultdict(int)
    #     for cube in cubes:
    #         a, color = cube.strip().split(" ")
    #         a = int(a)
    #         colors[color] += a
    #     if colors["red"] > 12 or colors["green"] > 13 or colors["blue"] > 14:
    #         possible = False
    #     maxs["red"] = max(colors["red"], maxs["red"])
    #     maxs["green"] = max(colors["green"], maxs["green"])
    #     maxs["blue"] = max(colors["blue"], maxs["blue"])
    # s += maxs["red"] * maxs["green"] * maxs["blue"]
    if possible:
        id = int(id.split()[1])
        s1 += id

if s2:
    print(s2)
    pyperclip.copy(s2)  # type:ignore
else:
    print(s1)
    pyperclip.copy(s1)  # type:ignore

if answer is not None:
    post_answer(day, 1, answer)
