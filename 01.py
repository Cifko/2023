from downloader import download, post_answer
from os.path import exists
from helper import *
import sys
import re
import pyperclip  # type:ignore

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
while data:
    next_line()
    # print(j, a)
    x = re.findall(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line)

    def to_num(x):
        if x == "one":
            return 1
        if x == "two":
            return 2
        if x == "three":
            return 3
        if x == "four":
            return 4
        if x == "five":
            return 5
        if x == "six":
            return 6
        if x == "seven":
            return 7
        if x == "eight":
            return 8
        if x == "nine":
            return 9
        return int(x)

    s += to_num(x[0]) * 10 + to_num(x[-1])
    # print(int(x[0]) * 10 + int(x[-1]))
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
print(s)
pyperclip.copy(s)  # type:ignore

if answer is not None:
    post_answer(day, 1, answer)
