# type:ignore
from downloader import download, post_answer
from os.path import exists
from helper import *
import sys
import re
import time
import pyperclip

# import pyperclip  # type:ignore
from collections import defaultdict

# pyperclip.copy("")  # type:ignore

# day = int(sys.argv[0].split("/")[-1].split(".")[0])
day = 5
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
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    # if j <= 10:
    # print(j, a)
    game = explode(line, [":", "|"])
    if line:
        if seeds == None:
            seeds = nums
        else:
            if nums:
                d[name] += [nums]
            else:
                name = tuple(a[0].split("-")[0::2])


def flatten(l):
    return [item for sublist in l for item in sublist]


class Permutation:
    def __init__(self, permutation):
        self.permutation = [range(start, end + 1) for start, end in permutation]

    def __repr__(self):
        return " ".join(f"{r.start}-{r.stop - 1}" for r in self.permutation)

    def join(self, other):
        self.permutation = [self.permutation[i.start] for i in other.permutation]


s1 = 10000000000
for seed in seeds:
    name = "seed"
    while name != "location":
        for xd in d:
            if xd[0] == name:
                name = xd[1]
                for nums in d[xd]:
                    if seed >= nums[1] and seed < nums[1] + nums[2]:
                        seed += nums[0] - nums[1]
                        break
    s1 = min(s1, seed)
s2 = 0
# print(seeds)
# while True:
#     name = "location"
#     seed = s2
#     while name != "seed":
#         for xd in d:
#             if xd[1] == name:
#                 name = xd[0]
#                 for nums in d[xd]:
#                     if seed >= nums[0] and seed < nums[0] + nums[2]:
#                         seed += nums[1] - nums[0]
#                         break
#     found = False
#     for s, l in zip(seeds[0::2], seeds[1::2]):
#         if seed >= s and seed < s + l:
#             found = True
#             break
#     if found:
#         break
#     s2 += 1

if s2:
    print(s2)
    print(time.time() - start)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    print(s1)
    pyperclip.copy(s1)  # type:ignore
    # post_answer(day, 1, answer)
