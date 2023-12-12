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


def sol1(line, index, nums, force=False):
    if nums[0] == 0:
        if len(nums) == 1:
            while index < len(line):
                if line[index] == "#":
                    return 0
                index += 1
            return 1
        if len(line) == index:
            return 0
        if line[index] == "#":
            return 0
        index += 1
        force = False
        nums = nums[1:]
    if not force:
        while index < len(line) and line[index] == ".":
            index += 1
    s = 0
    if len(line) == index:
        return 0
    if line[index] == "?":
        if force:
            s += sol1(line, index + 1, [nums[0] - 1] + nums[1:], True)
        else:  # skip
            s += sol1(line, index + 1, nums, False)
            s += sol1(line, index + 1, [nums[0] - 1] + nums[1:], True)
    elif line[index] == "#":
        s += sol1(line, index + 1, [nums[0] - 1] + nums[1:], True)
    else:
        return 0
    return s


last_line = None
s1 = s2 = x = 0
grid = Grid()
col_cnt = defaultdict(int)
while data:
    next_line()
    print(s)
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    s = sol1("?".join([a[0]] * 5), 0, nums * 5)
    s1 += s

print("Part 1:", s1)
pyperclip.copy(s1)  # type:ignore
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    pass
    # post_answer(day, 1, answer)
