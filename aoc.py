from typing import Callable, Any
from collections import defaultdict as dd
from enum import Enum
import heapq
from snailfish import SnailFish

# import msvcrt as m
import sys

cross4: Callable[[int, int], list[tuple[int, int]]] = lambda x, y: [
    (x, y - 1),
    (x - 1, y),
    (x + 1, y),
    (x, y + 1),
]
cross5: Callable[[int, int], list[tuple[int, int]]] = lambda x, y: [
    (x, y - 1),
    (x - 1, y),
    (x, y),
    (x + 1, y),
    (x, y + 1),
]
cross8: Callable[[int, int], list[tuple[int, int]]] = lambda x, y: [
    (x - 1, y),
    (x + 1, y),
    (x, y - 1),
    (x, y + 1),
    (x - 1, y - 1),
    (x - 1, y + 1),
    (x + 1, y - 1),
    (x + 1, y + 1),
]
cross9: Callable[[int, int], list[tuple[int, int]]] = lambda x, y: [
    (x - 1, y - 1),
    (x, y - 1),
    (x + 1, y - 1),
    (x - 1, y),
    (x, y),
    (x + 1, y),
    (x - 1, y + 1),
    (x, y + 1),
    (x + 1, y + 1),
]

inside: Callable[[int, int, int, int], bool] = lambda x, y, w, h: 0 <= x < w and 0 <= y < h
triangle: Callable[[int], int] = lambda x: x * (x + 1) // 2
add_border: Callable[[list[list[str]], str], list[list[str]]] = lambda A, border: [
    [*row, border] for row in [*A, [border] * len(A[0])]
]
manhattan2: Callable[[list[int], list[int]], int] = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
manhattan3: Callable[[list[int], list[int]], int] = (
    lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
)


def replace_str(A: list[str] | str, old: str, new: Any) -> list[str] | str:
    if isinstance(A, list):
        return [replace_str(a, old, new) for a in A]
    if A == old:
        return new
    return A


def find_pair(X: Any, key: Callable[[Any, Any], int]) -> tuple[Any, int, int]:
    sol = None
    for i, a in enumerate(X):
        for j, b in enumerate(X):
            if i != j:
                v = key(a, b)
                if sol is None or sol[0] < v:
                    sol = (v, i, j)
    return sol


def grid_to_edges(w, h, cross_function=cross4):
    edges = dd(list)
    for i in range(w):
        for j in range(h):
            for x, y in cross_function(i, j):
                if 0 <= x < w and 0 <= y < h:
                    edges[(i, j)] += [(x, y)]
    return edges


# def multi_range()


def djikstra(edges, start, end, value_fn, start_value=None):
    update = lambda value, next_value: value + value_fn(next_value)
    if start_value is None:
        start_value = value_fn(start)
    stack = [(start_value, start, 0)]
    distance = dd(lambda: -1)
    data = dd(lambda: float("inf"))
    while stack:
        r, pos, steps = heapq.heappop(stack)
        if distance[pos] >= 0:
            continue
        distance[pos] = steps
        if data[pos] <= r:
            continue
        data[pos] = r
        if pos == end:
            break
        for next in edges[pos]:
            heapq.heappush(stack, (update(r, next), next, steps + 1))
    return data


def find_path(edges, start, end, data):
    pos = end
    path = []
    while pos != start:
        path.append(pos)
        next_val = float("inf")
        next_pos = None
        for next in edges[pos]:
            if next_val > data[next]:
                next_val = data[next]
                next_pos = next
        pos = next_pos
    path.append(pos)
    return path


pop_stack: Callable[[list[Any]], Any] = lambda stack: stack.pop()
push_stack: Callable[[list[Any], Any], None] = lambda stack, item: stack.append(item)


class Stack:
    def __init__(self, initItem: Any, is_heap: bool = True):
        self.stack: list[Any] = [initItem]
        if is_heap:
            self.pop_function = heapq.heappop
            self.push_function = heapq.heappush
        else:
            self.pop_function = pop_stack
            self.push_function = push_stack

    def isNotEmpty(self) -> bool:
        return not self.isEmpty()

    def isEmpty(self) -> bool:
        return not self.stack

    def pop(self) -> Any:
        return self.pop_function(self.stack)

    def push(self, item: Any) -> None:
        self.push_function(self.stack, item)

    def __iadd__(self, item: Any) -> None:
        self.push(item)


class Vector2D:
    def __init__(
        self,
        x: int | tuple[int, int] | list[int],
        y: int | None = None,
    ):
        if isinstance(x, tuple) or isinstance(x, list):
            self.from_tuple(tuple(x))
        else:
            self.from_xy(x, y)

    def from_tuple(self, pos: tuple[int]):
        self.pos = pos

    def from_xy(self, x: int, y: int):
        self.pos = (x, y)

    def __str__(self):
        return f"({self.pos[0]}, {self.pos[1]})"

    def __repr__(self):
        return str(self)

    # HELPER FUNCTIONs
    def manhattan(self, other: "Vector2D") -> int:
        return abs(self.pos[0] - other.pos[0]) + abs(self.pos[1] - other.pos[1])

    # OPERATORs

    def __add__(self, other: "Vector2D"):
        return Vector2D(
            self.pos[0] + other.pos[0],
            self.pos[1] + other.pos[1],
        )

    def __iadd__(self, other: "Vector2D"):
        self.pos[0] += other.pos[0]
        self.pos[1] += other.pos[1]

    def __sub__(self, other: "Vector2D"):
        return Vector2D(
            self.pos[0] - other.pos[0],
            self.pos[1] - other.pos[1],
        )

    def __isub__(self, other: "Vector2D"):
        self.pos[0] -= other.pos[0]
        self.pos[1] -= other.pos[1]

    def __mul__(self, other: "Vector2D") -> int:
        return self.pos[0] * other.pos[0] + self.pos[1] * other.pos[1]

    def __hash__(self):
        print(self.pos)
        return hash(self.pos)

    def __eq__(self, other: "object") -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.pos[0] == other.pos[0] and self.pos[1] == other.pos[1]

    # SETTER & GETTERS

    def set_x(self, value: int) -> None:
        self.pos[0] = value

    def get_x(self) -> int:
        return self.pos[0]

    def set_y(self, value: int) -> None:
        self.pos[1] = value

    def get_y(self) -> int:
        return self.pos[1]

    def set_z(self, value: int) -> None:
        self.pos[2] = value

    def __getitem__(self, key: int) -> int:
        return self.pos[key]

    x = property(get_x, set_x)
    y = property(get_y, set_y)


class Vector3D:
    def __init__(
        self,
        x: int | tuple[int, int, int] | list[int],
        y: int | None = None,
        z: int | None = None,
    ):
        if isinstance(x, tuple) or isinstance(x, list):
            self.from_tuple(tuple(x))
        else:
            self.from_xyz(x, y, z)

    def from_tuple(self, pos: tuple[int, int, int]):
        self.pos = pos

    def from_xyz(self, x: int, y: int, z: int):
        self.pos = (x, y, z)

    def __str__(self):
        return f"({self.pos[0]}, {self.pos[1]}, {self.pos[2]})"

    def __repr__(self):
        return str(self)

    # HELPER FUNCTIONs
    def manhattan(self, other: "Vector3D") -> int:
        return (
            abs(self.pos[0] - other.pos[0])
            + abs(self.pos[1] - other.pos[1])
            + abs(self.pos[2] - other.pos[2])
        )

    # OPERATORs

    def __add__(self, other: "Vector3D"):
        return Vector3D(
            self.pos[0] + other.pos[0],
            self.pos[1] + other.pos[1],
            self.pos[2] + other.pos[2],
        )

    def __iadd__(self, other: "Vector3D"):
        self.pos = (
            self.pos[0] + other.pos[0],
            self.pos[1] + other.pos[1],
            self.pos[2] + other.pos[2],
        )

    def __sub__(self, other: "Vector3D"):
        return Vector3D(
            self.pos[0] - other.pos[0],
            self.pos[1] - other.pos[1],
            self.pos[2] - other.pos[2],
        )

    def __isub__(self, other: "Vector3D"):
        self.pos = (
            self.pos[0] - other.pos[0],
            self.pos[1] - other.pos[1],
            self.pos[2] - other.pos[2],
        )

    def __mul__(self, other: "Vector3D") -> int:
        return self.pos[0] * other.pos[0] + self.pos[1] * other.pos[1] + self.pos[2] * other.pos[2]

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other: "object") -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.pos[0] == other.pos[0]
            and self.pos[1] == other.pos[1]
            and self.pos[2] == other.pos[2]
        )

    # SETTER & GETTERS

    def set_x(self, value: int) -> None:
        self.pos = (value, self.pos[1], self.pos[2])

    def get_x(self) -> int:
        return self.pos[0]

    def set_y(self, value: int) -> None:
        self.pos = (self.pos[0], value, self.pos[2])
        self.pos[1] = value

    def get_y(self) -> int:
        return self.pos[1]

    def set_z(self, value: int) -> None:
        self.pos = (self.pos[0], self.pos[1], value)

    def get_z(self) -> int | None:
        return self.pos[2]

    def __getitem__(self, key: int) -> int:
        return self.pos[key]

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)


inside2D = (
    lambda x0, x1, y0, y1, px0, px1, py0, py1: px0 <= x0 <= x1 <= px1 and py0 <= y0 <= y1 <= py1
)

inside3D = (
    lambda x0, x1, y0, y1, z0, z1, px0, px1, py0, py1, pz0, pz1: px0 <= x0 <= x1 <= px1
    and py0 <= y0 <= y1 <= py1
    and pz0 <= z0 <= z1 <= pz1
)

disjoint2D = (
    lambda x0, x1, y0, y1, px0, px1, py0, py1: x1 <= px0 or px1 <= x0 or y1 <= py0 or py1 <= y0
)
disjoint3D = (
    lambda x0, x1, y0, y1, z0, z1, px0, px1, py0, py1, pz0, pz1: x1 <= px0
    or px1 <= x0
    or y1 <= py0
    or py1 <= y0
    or z1 <= pz0
    or pz1 <= z0
)


class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def clear_console():
    print("\x1Bc", end="")
    print("\x1b[?25l", end="")


def move_cursor(y, x):
    print("\033[%d;%dH" % (y + 1, x + 1), end="")


def wait_for_key():
    sys.stdout.flush()
    # if m.getch() == b"\x03":
    #     exit()


def print_on_pos(y, x, text):
    print(f"\033[{y+1};{x+1}H{text}")
