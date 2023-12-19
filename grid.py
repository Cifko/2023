from typing import Any, Iterable, Callable, Optional, Hashable, Generator
from downloader import download
import re
import heapq


class Pos:
    def __init__(self, x: int, y: int, score: Any = 0, c: int = 0, dx: int = 0, dy: int = 0, path: list[tuple[int, int]] = [], backpack: tuple[Any, ...] = ()):
        self._x = x
        self._y = y
        self._c = c
        self._dx = dx
        self._dy = dy
        self._path = path
        self._backpack = backpack
        self.score = score

    def get_next(self, nx: int, ny: int) -> "Pos":
        if nx == self.x + self.dx and ny == self.y + self.dy:
            nc = self.c + 1
        else:
            nc = 1
        return Pos(nx, ny, self.score, nc, nx - self.x, ny - self.y, self.path + [(self.x, self.y)], self.backpack)

    def same_dir(self, other: "Pos") -> bool:
        return other.dx == self.dx and other.dy == self.dy

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def c(self) -> int:
        return self._c

    @property
    def dx(self) -> int:
        return self._dx

    @property
    def dy(self) -> int:
        return self._dy

    @property
    def path(self) -> list[tuple[int, int]]:
        return self._path

    @property
    def backpack(self) -> tuple[Any, ...]:
        return self._backpack

    @property
    def score(self) -> Any:
        return self._score

    @score.setter
    def score(self, value: Any):
        self._score = value

    def __lt__(self, other: "Pos"):
        return self.score < other.score

    def __str__(self):
        return f"({self.x}, {self.y}) {self.score} {self.backpack}"

    def __repr__(self):
        return self.__str__()


class Grid[V]:
    def __init__(self):
        self._width = 0
        self._height = 0
        self.cells: list[list[V]] = []
        self._get: Callable[[int, int], Generator[tuple[int, int], None, None]] = self.get4

    @property
    def get(self) -> Callable[[int, int], Generator[tuple[int, int], None, None]]:
        return self._get

    @get.setter
    def get(self, value: Callable[[int, int], Generator[tuple[int, int], None, None]]):
        self._get = value

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def add_row(self, row: Iterable[V]):
        self.cells.append(list(row))
        if self.height > 0:
            if len(self.cells[-1]) != self.width:
                raise Exception("Row width mismatch")
        else:
            self._width = len(self.cells[-1])
        self._height += 1

    def __str__(self):
        return "\n".join(["".join(map(str, row)) for row in self.cells])

    def __repr__(self) -> str:
        return self.__str__()

    def get4(self, x: int, y: int) -> Generator[tuple[int, int], None, None]:
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                yield nx, ny

    def get8(self, x: int, y: int) -> Generator[tuple[int, int], None, None]:
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)]:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                yield nx, ny

    def djikstra(
        self,
        start: Pos,
        next: Callable[[Pos, Pos], Optional[Pos]],
        is_end: Callable[[Pos], bool],
        cache_key: Callable[[Pos], Hashable] = lambda pos: (pos.x, pos.y, pos.backpack),
    ) -> Optional[Pos]:
        heap: list[Pos] = [start]
        cache: set[Hashable] = set()
        while heap:
            pos = heapq.heappop(heap)
            key = cache_key(pos)
            if key in cache:
                continue
            cache.add(key)
            if is_end(pos):
                return pos
            for nx, ny in self._get(pos.x, pos.y):
                next_pos = next(pos, pos.get_next(nx, ny))
                if next_pos:
                    heapq.heappush(heap, next_pos)
        return None

    def is_last(self, pos: Pos):
        return pos.x == self.width - 1 and pos.y == self.height - 1

    def __iter__(self) -> Generator[tuple[int, int, V], None, None]:
        for y, line in enumerate(self.cells):
            for x, cell in enumerate(line):
                yield (x, y, cell)

    @property
    def size(self) -> int:
        return self.width * self.height

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

    def add_border(self, value: V):
        for i in range(self._height):
            self.cells[i].insert(0, value)
            self.cells[i].append(value)
        self._width += 2
        self.cells.insert(0, [value] * self._width)
        self.cells.append([value] * self._width)
        self._height += 2

    def flood_fill(self, x: int, y: int, value: Any) -> int:
        initial_value = self.grid[y][x]
        next = [(x, y)]
        filled = 0
        while next:
            x, y = next.pop()
            if self.grid[y][x] != initial_value:
                continue
            self.grid[y][x] = value
            filled += 1
            next.extend(self._get(x, y))
        return filled

    def map(self, fn: Callable[[V], V]):
        for x, y, value in self:
            self.cells[y][x] = fn(value)

    def add(self, value: Any):
        self.map(lambda x: x + value)

    def sub(self, value: Any):
        self.map(lambda x: x - value)

    def mul(self, value: Any):
        self.map(lambda x: x * value)

    def div(self, value: Any):
        self.map(lambda x: x // value)

    def divf(self, value: Any):
        self.map(lambda x: x / value)

    def transpose(self):
        self._width, self._height = self._height, self._width
        self.grid = zip(*self.grid)

    def find_one(self, value: V) -> Optional[tuple[int, int]]:
        for x, y, val in self:
            if val == value:
                return (x, y)

    def find_all(self, value: V) -> Generator[tuple[int, int], None, None]:
        for x, y, val in self:
            if val == value:
                yield (x, y)


def ss(g: Grid[int]):
    def next(u: Pos, v: Pos) -> Optional[Pos]:
        if u.dx == -v.dx and u.dy == -v.dy:
            return None
        if v.c > 3:
            return None
        v.score += g.cells[v.y][v.x]
        return v

    def next2(u: Pos, v: Pos) -> Optional[Pos]:
        if u.dx == -v.dx and u.dy == -v.dy:
            return None
        if v.c > 10:
            return None
        if u.c < 4 and not u.same_dir(v) and u.score > 0:
            return None
        v.score += g.cells[v.y][v.x]
        return v

    if s := g.djikstra(Pos(0, 0), next, g.is_last, lambda pos: (pos.x, pos.y, pos.c, pos.dx, pos.dy)):
        print(s.score)
    if s := g.djikstra(Pos(0, 0), next2, lambda pos: g.is_last(pos) and pos.c >= 4, lambda pos: (pos.x, pos.y, pos.c, pos.dx, pos.dy)):
        print(s.score)
    # for x, y, c in g:
    #     print(c, end="")
    #     if x == g.width - 1:
    #         print()


day = 17
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


g: Grid[int] = Grid()
while data:
    next_line()
    # beware parsing line with single value, where it can be text or int and you expect int (because a will be int in this case), use 'line' instead
    g.add_row(map(int, line))


ss(g)
