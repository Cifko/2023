# type:ignore
from downloader import download, post_answer
from os.path import exists
from helper import *
import sys
import re
import pyperclip  # type:ignore
from collections import defaultdict
from copy import copy

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


def apply_rule(x, m, a, s, rule):
    if ":" not in rule:
        return rule
    r, p = rule.split(":", 1)
    q, p = p.split(",", 1)
    if eval(r):
        return apply_rule(x, m, a, s, q)
    else:
        return apply_rule(x, m, a, s, p)


answer = None
s = x = 0

last_line = None
s1 = s2 = x = 0
grid = Grid()
col_cnt = defaultdict(int)
rules = {}
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    if line == "":
        break
    line = line.rstrip("}")
    part, line = line.split("{")
    rules[part] = line

while data:
    next_line()
    x, m, a, s = nums
    r = "in"
    while r not in ["R", "A"]:
        r = apply_rule(x, m, a, s, rules[r])
    if r == "A":
        s1 += sum(nums)


def apply_rule(xmas: Intervals, rule: str):
    if not all(xmas):
        return []
    if ":" not in rule:
        match rule:
            case "A":
                return [xmas]
            case "R":
                return []
            case _:
                return apply_rule(xmas, rules[rule])
    op, branches = rule.split(":", 1)
    true_branch, false_branch = branches.split(",", 1)
    res = []
    i = "xmas".find(op[0])
    value = eval(op[2:])
    match op[1]:
        case "<":
            oxmas = copy(xmas)
            xmas[i] = xmas[i] < value
            res += apply_rule(xmas, true_branch)
            xmas = oxmas
            xmas[i] = xmas[i] >= value
            res += apply_rule(xmas, false_branch)
        case ">":
            oxmas = copy(xmas)
            xmas[i] = xmas[i] > value
            res += apply_rule(xmas, true_branch)
            xmas = oxmas
            xmas[i] = xmas[i] <= value
            res += apply_rule(xmas, false_branch)
        case _:
            raise Exception("Unknown rule")
    return res


r = apply_rule([Intervals([(1, 4000)]) for _ in range(4)], rules["in"])
for x, m, a, s in r:
    s2 += (x[0][1] - x[0][0] + 1) * (m[0][1] - m[0][0] + 1) * (a[0][1] - a[0][0] + 1) * (s[0][1] - s[0][0] + 1)

print("Part 1:", s1)
pyperclip.copy(s1)  # type:ignore
if s2:
    print("Part 2:", s2)
    pyperclip.copy(s2)  # type:ignore
    # post_answer(day, 2, answer)
else:
    pass
    # post_answer(day, 1, answer)
