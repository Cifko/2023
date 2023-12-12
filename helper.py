# Importing necessary libraries
from collections import defaultdict as dd
import heapq
from time import time
from typing import Any, Iterator, Callable, TypeVar, Hashable, Protocol


# type VALUE = SupportsRichComparisonT


# Defining a class for MaxHeap
class MaxHeap:
    # Constructor for MaxHeap
    def __init__(self):
        self.items: list[Any] = [None] * 1000002
        self.size: int = 0

    # Function to add an item to the heap
    def push(self, item: Any) -> None:
        # Adding the item at the end of the heap
        self.items[self.size] = item
        # Getting the index of the item
        i = self.size
        # Calculating the parent index
        parent = (i - 1) // 2
        # Loop to percolate up the item to its correct position
        while i > 0 and self.items[parent] < self.items[i]:
            # Swapping the item with its parent if it is greater than the parent
            self.items[parent], self.items[i] = self.items[i], self.items[parent]
            # Updating the index to parent's index
            i = parent
            # Recalculating the parent index
            parent = (i - 1) // 2
        # Increasing the size of the heap
        self.size += 1

    # Function to remove and return the maximum item from the heap
    def pop(self):
        # If heap is empty, raise an error
        if self.size <= 0:
            raise BaseException("Empty heap")
        # If heap has only one item, return that item
        if self.size == 1:
            self.size = 0
            return self.items[0]
        # Store the maximum item
        root = self.items[0]
        # Decrease the size of the heap
        self.size -= 1
        # Replace the root of the heap with the last item
        self.items[0] = self.items[self.size]
        # Heapify the root item
        self.heapify(0)
        # Return the maximum item
        return root

    # Function to percolate down an item to its correct position
    def heapify(self, index: int):
        while True:
            # Calculate the indices of the left and right children
            left = (index << 1) + 1
            right = (index << 1) + 2
            # Assume the item is in its correct position
            smallest = index
            # If the right child exists
            if right < self.size:
                # If the left child is greater than the item, update the smallest index
                if self.items[left] > self.items[index]:
                    smallest = left
                # If the right child is greater than the current smallest, update the smallest index
                if self.items[right] > self.items[smallest]:
                    smallest = right
            else:
                # If only the left child exists and it is greater than the item, update the smallest index
                if left < self.size and self.items[left] > self.items[index]:
                    smallest = left
            # If the smallest index is not the item's index, swap them
            if smallest != index:
                self.items[smallest], self.items[index] = self.items[index], self.items[smallest]
                # Update the index to the smallest index
                index = smallest
            else:
                # If the item is in its correct position, break the loop
                break

    # Function to represent the heap as a string
    def __repr__(self):
        return f"({len(self.items)}) {self.items}"


class Grid:
    def __init__(self):
        print("Grid is y,x not x,y")
        self._width = self._height = 0
        self.grid = []

    def add_border(self, value: Any):
        self.grid = [[value] * self._width] + self.grid + [[value] * self._width]
        for i, line in enumerate(self.grid):
            self.grid[i] = [value] + line + [value]
        self._width += 2
        self._height += 2

    def upscale3x3(self, upscale: Any):
        self._width *= 3
        self._height *= 3
        new_grid = [[None] * self._width for _ in range(self._height)]
        for y, line in enumerate(self.grid):
            for x, cell in enumerate(line):
                up = upscale(cell)
                for dy in range(3):
                    for dx in range(3):
                        new_grid[y * 3 + dy][x * 3 + dx] = up[dy][dx]
        self.grid = new_grid

    def add_char_line(self, line):
        self._height += 1
        self.grid.append(list(line))
        self._width = len(self.grid[-1])

    def add_int_line(self, line):
        self._height += 1
        self.grid.append(list(map(int, line)))
        self._width = len(self.grid[-1])

    def __repr__(self):
        res = f"H({self._height}) x W({self._width})\n"
        res += "\n".join("".join(map(str, line)) for line in self.grid)
        return res

    def get_size(self):
        return self._width * self._height

    def enumerate(self):
        for y, line in enumerate(self.grid):
            for x, cell in enumerate(line):
                yield (x, y, cell)

    def flood_fill(self, x: int, y: int, value):
        initial_value = self.grid[y][x]
        next = [(x, y)]
        filled = 0
        while next:
            x, y = next.pop()
            if self.grid[y][x] != initial_value:
                continue
            self.grid[y][x] = value
            filled += 1
            next.extend(self.get4(x, y))
        return filled

    def map(self, fn):
        for x, y, value in self.enumerate():
            self.grid[y][x] = fn(value)

    def get4(self, x, y):
        return [(nx, ny) for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if 0 <= nx < self._width and 0 <= ny < self._height]

    def get8(self, x, y):
        return [
            (nx, ny)
            for nx, ny in [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
            if 0 <= nx < self._width and 0 <= ny < self._height
        ]

    def inc(self):
        self.map(lambda x: x + 1)

    def dec(self):
        self.map(lambda x: x - 1)

    def add(self, value):
        self.map(lambda x: x + value)

    def sub(self, value):
        self.map(lambda x: x - value)

    def mul(self, value):
        self.map(lambda x: x * value)

    def div(self, value):
        self.map(lambda x: x // value)

    def divf(self, value):
        self.map(lambda x: x / value)

    def __getitem__(self, key):
        if type(key) == int:
            return self.grid[key]
        if type(key) == tuple and len(key) == 2:
            if type(key[1]) == slice:
                return [row[key[0]] for row in self.grid[key[1]]]
            return self.grid[key[1]][key[0]]
        raise Exception("__getitem__ wrong key {key}")

    def __setitem__(self, key, value):
        if type(key) == tuple and len(key) == 2:
            self.grid[key[1]][key[0]] = value
            return value
        raise Exception(f"__setitem__ wrong key {key}")

    def get_row(self, row):
        return self.grid[row]

    def get_col(self, col):
        return self[col, :]

    def inverse(self):
        self._width, self._height = self._height, self._width
        self.grid = zip(*self.grid)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def gen_graph(self):
        graph = Graph()
        for x, y, value in self.enumerate():
            graph.add_vertex((x, y), value)
            if 0 < x:
                graph.add_edge((x - 1, y), (x, y))
            if 0 < y:
                graph.add_edge((x, y - 1), (x, y))
        return graph

    def find_one(self, value):
        for x, y, val in self.enumerate():
            if val == value:
                return (x, y)

    def find_all(self, value):
        for x, y, val in self.enumerate():
            if val == value:
                yield (x, y)

    size = property(get_size)
    width = property(get_width)
    height = property(get_height)


class Instant:
    def __init__(self):
        self.time = time()

    def __repr__(self):
        return f"{time()-self.time}"


class Timer:
    def __init__(self):
        self.total_time = 0
        self.counter = 0
        self.start_time = None

    def start(self):
        self.start_time = time()

    def stop(self):
        self.total_time += time() - self.start_time
        self.start_time = None
        self.counter += 1

    def __repr__(self):
        return f"Time : {self.total_time} Counter : {self.counter}"


class MinMax:
    def __init__(self):
        self.dict_values = {}
        self.list_values = []

    def add(self, *args, **kwargs):
        # print(args, kwargs)
        # if len(args) == 1 and type(args) != tuple:
        if len(args) == 1:
            if type(args[0]) == list:
                args = args[0]
            elif isinstance(args[0], Vector):
                args = args[0].v
            else:
                raise Exception(f"Unknown type send to MinMax::add {type(args[0])})")
        for i, arg in enumerate(args):
            if len(self.list_values) == i:
                self.list_values.append((arg, arg))
            else:
                self.list_values[i] = (min(self.list_values[i][0], arg), max(self.list_values[i][1], arg))
        for key in kwargs:
            if key not in self.dict_values:
                self.dict_values[key] = (kwargs[key], kwargs[key])
            else:
                self.dict_values[key] = (min(kwargs[key], self.dict_values[key][0]), max(kwargs[key], self.dict_values[key][1]))

    def add_val(self, value):
        self.list_values = [(x[0] - value, x[1] + value) for x in self.list_values]

    def sub_val(self, value):
        self.add_val(-value)

    def inc(self):
        self.add_val(1)

    def dec(self):
        self.sub_val(1)

    def get_val(self, is_max, *args, **kwargs):
        if len(args) + len(kwargs) != 1:
            raise Exception(f"Wrong number of args for min args ({args}, {kwargs})")
        if args:
            return self.list_values[args[0]][is_max]

    def min(self, *args, **kwargs):
        return self.get_val(False, *args, **kwargs)

    def max(self, *args, **kwargs):
        return self.get_val(True, *args, **kwargs)

    min_x = property(lambda self: self.min(0))
    max_x = property(lambda self: self.max(0))
    min_y = property(lambda self: self.min(1))
    max_y = property(lambda self: self.max(1))
    min_z = property(lambda self: self.min(2))
    max_z = property(lambda self: self.max(2))

    def __repr__(self):
        return f"MinMax {self.list_values} {self.dict_values}"

    def min_to_vec(self):
        return Vector([x[0] for x in self.list_values])

    def max_to_vec(self):
        return Vector([x[1] for x in self.list_values])

    # def min_to_vec3(self):
    #     if self.dict_values:
    #         raise "There are dict values in MinMax, can't convert to Vector3"
    #     if len(self.list_values) != 3:
    #         raise "There are not exactly 3 list values, can't convert MinMax to Vector3"
    #     return Vector3(self.list_values[0][0], self.list_values[1][0], self.list_values[2][0])

    # def max_to_vec3(self):
    #     if self.dict_values:
    #         raise "There are dict values in MinMax, can't convert to Vector3"
    #     if len(self.list_values) != 3:
    #         raise "There are not exactly 3 list values, can't convert MinMax to Vector3"
    #     return Vector3(self.list_values[0][1], self.list_values[1][1], self.list_values[2][1])


class Vector:
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args, tuple) or isinstance(args, list):
                args = args[0]
            if isinstance(args, Vector):
                args = args.v
        self.v = tuple(args)
        # print("args", args)
        self.size = len(self.v)

    def get_around_single(self, include_self=False):
        if include_self:
            yield self
        for i, val in enumerate(self.v):
            yield Vector(self.v[:i] + (val - 1,) + self.v[i + 1 :])
            yield Vector(self.v[:i] + (val + 1,) + self.v[i + 1 :])

    def get_around_all(self, include_self=False):
        return self.get_cube(1, include_self)

    def get_cube(self, distance, include_self=False):
        for x in range(not include_self, 3**self.size):
            a = []
            res = Vector(self)
            for i, v in enumerate(self.v):
                a.append([v, v - 1, v + 1][x % 3])
                x //= 3
            yield Vector(a)

    def __eq__(self, other):
        return self.v == other.v

    def __hash__(self):
        return hash(self.v)

    def __getitem__(self, index):
        return self.v[index]

    def __repr__(self):
        return f"({', '.join(map(str,self.v))})"

    def in_range(self, ranges):
        return all(r[0] <= v <= r[1] for v, r in zip(self.v, ranges))

    def manhattan(self, other):
        return sum(abs(v - o) for v, o in zip(self.v, other.v))

    def gen_area(self, distance_left, index=0):
        if index == self.size - 1:
            yield (self.v[index] + distance_left,)
            if distance_left > 0:
                yield (self.v[index] - distance_left,)
            return
        for i in range(distance_left + 1):
            for x in self.gen_area(distance_left - i, index + 1):
                yield (self.v[index] + i, *x)
                if i > 0:
                    yield (self.v[index] - i, *x)

    def get_diamond_area(self, distance):
        for pos in self.gen_area(distance):
            yield Vector(pos)

    def gen_volume(self, distance_left, index=0):
        if index == self.size - 1:
            for i in range(distance_left):
                yield (self.v[index] + i,)
                if i > 0:
                    yield (self.v[index] - i,)
            return
        for i in range(distance_left + 1):
            for x in self.gen_volume(distance_left - i, index + 1):
                yield (self.v[index] + i, *x)
                if i > 0:
                    yield (self.v[index] - i, *x)

    def get_diamond_volume(self, distance, include_self=False):
        for pos in self.gen_volume(distance):
            if pos != self.v or include_self:
                yield Vector(pos)


class Intervals:
    # Integers numbers coverage. So if you add (1,3) and (4,5) that means all numbers from 1 to 5 are covered
    def __init__(self):
        self.intervals: list[tuple[int, int]] = []

    def add(self, start: int, end: int, include_reverse: bool = False):
        if start > end and not include_reverse:
            return
        new_intervals: list[tuple[int, int]] = []
        merge_start = merge_end = None
        added = False
        for s, e in self.intervals:
            if e + 1 < start:
                new_intervals += [(s, e)]
            elif s > end + 1:
                if merge_start is not None and merge_end is not None:
                    new_intervals += [(merge_start, merge_end)]
                    added = True
                    merge_start = None
                if not added:
                    new_intervals += [(start, end)]
                    added = True
                new_intervals += [(s, e)]
            else:
                if merge_start is None:
                    merge_start = min(s, start)
                if merge_end is None:
                    merge_end = max(e, end)
                else:
                    merge_end = max(e, merge_end)
        if not added:
            if merge_start is not None and merge_end is not None:
                new_intervals += [(merge_start, merge_end)]
            else:
                new_intervals += [(start, end)]
        self.intervals = new_intervals

    def get_gaps(self) -> int:
        # return the number of numbers not covered between min and max of these intervals
        last = None
        gaps = 0
        for x, y in self.intervals:
            if last is not None:
                gaps += x - last - 1
            last = y
        return gaps


# x = Graph[int, str]()
# x.add_vertex(0, "a")
# x.add_vertex(1, "b")
# x.add_vertex(2, "c")
# x.add_edge(0, 1, 3.5)
# x.add_edge(0, 2, 1.5)
# x.add_edge(1, 2, 1.5)

# print(x.djikstra(0, update_backpack=lambda x: set([x])))

# from typing import TypeVar, Protocol, Hashable


# class ComparableHashable(Hashable, Protocol):
#     def __lt__(self, other: "ComparableHashable") -> bool:
#         ...


# T = TypeVar("T", bound=ComparableHashable)


# def f(x: list[T]) -> list[T]:
#     return sorted(set(x))
