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
cards = []
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    game = explode(line, [":", "|"])
    cards += [a]


def val(hand):
    x = defaultdict(int)
    for c in hand:
        x[c] += 1
    if 5 in x.values():
        return 7
    if 4 in x.values():
        return 6
    if 3 in x.values() and 2 in x.values():
        return 5
    if 3 in x.values():
        return 4
    if list(x.values()).count(2) == 2:
        return 3
    if 2 in x.values():
        return 2
    return 1


def value(hand):
    m = 0
    if "J" in hand:
        for c in "23456789TQKA":
            hand2 = hand
            hand2 = hand2.replace("J", c)
            m = max(m, val(hand2))
        return m
    return val(hand)


def value2(hand):
    return list(map(lambda x: "J23456789TQKA".find(x), hand))


cards = sorted(cards, key=lambda x: (value(str(x[0])), value2(str(x[0]))))
s1 = 0
for i, c in enumerate(cards):
    s1 += c[1] * (i + 1)
    print(c[0], c[1], i + 1)
# print(s1)

if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    print("Part 1:", s1)
    pyperclip.copy(s1)  # type:ignore
    # post_answer(day, 1, answer)
