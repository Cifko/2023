# type:ignore
from downloader import download, post_answer
from os.path import exists
from collections import defaultdict as dd
import sys
import re
from copy import deepcopy
from math import gcd, lcm
from helper import Graph, Grid

day = int(sys.argv[0].split("/")[-1].split(".")[0])
file_name = f"{day:02}-input.txt"
sample_file_name = f"{day:02}-input.txt"
if not exists(file_name):
    download(day)
f = open(file_name)


def parse_value(x: str):
    try:
        return int(x)
    except:
        return x


def parse(line: str):
    A = [parse_value(x) for x in line.split()]
    if len(A) == 1:
        A = A[0]
    nums = list(map(int, re.findall("(-?\d+)", line)))
    return (A, line, nums)

A = [parse(line.rstrip()) for line in f.readlines()]


a = line = nums = None
j = -1


def next_line():
    global A, a, line, nums, j
    a, line, nums = A.pop(0)
    j += 1


graph = Graph()
grid = Grid()
s = e = None
while A:
    next_line()
    print(a, line, nums)
    # grid.add_char_line(line)
    # grid.add_int_line(line)
    # grid.add_int_line(nums)


# s = grid.find_one("S")
# e = grid.find_one("E")
# grid[s] = "a"
# grid[e] = "z"
# graph = grid.gen_graph()

# w = graph.djikstra(s, 0, can_move_between=lambda u, v, backpack: ord(u) + 1 >= ord(v))
# print(r := graph.get_min_for(e))
# w = graph.djikstra(e, 0, can_move_between=lambda u, v, backpack: ord(v) + 1 >= ord(u))
# print(r := graph.get_min_for_value("a"))


# w = graph.djikstra(s, 0, can_move_between=lambda u, v, backpack: u + 1 >= v)
# print(graph.get_min_for(e))
# w = graph.djikstra(e, 0, can_move_between=lambda u, v, backpack: v + 1 >= u)
# print(r:=graph.get_min_for_value(ord("a")))

post_answer(day, 1, r)
