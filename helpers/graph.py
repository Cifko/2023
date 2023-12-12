# Importing necessary libraries
from collections import defaultdict as dd
import heapq
from typing import Any, Iterator, Callable, Hashable, Protocol, Optional


class ComparableHashable(Hashable, Protocol):
    def __lt__(self, other: "ComparableHashable") -> bool:
        ...


type Backpack[VALUE] = tuple[VALUE, ...]  # A tuple representing the "backpack" of items
type CanMoveBetween[VALUE] = Callable[
    [Optional[VALUE], Optional[VALUE], Backpack[VALUE]], bool
]  # A function to determine if a move is possible between two vertices
type CanMoveTo[VALUE] = Callable[[Optional[VALUE], Backpack[VALUE]], bool]  # A function to determine if a move is possible to a vertex
type UpdateBackpack[VALUE] = Callable[[Optional[VALUE]], set[VALUE]]  # A function to update the "backpack"
type DjikstraSolution[VALUE, VERTEX] = dict[VERTEX, dict[Backpack[VALUE], float]]  # A dictionary representing the solution to Dijkstra's algorithm


class Graph[VERTEX, VALUE: ComparableHashable]:
    # Constructor for the Graph class
    def __init__(self):
        # Initialize 'edges' as a nested dictionary using defaultdict.
        # The outer dictionary's keys represent source vertices and the inner dictionary's keys represent destination vertices.
        # The value of the inner dictionary represents the weight of the edge between the source and destination vertices.
        self.edges: dict[VERTEX, dict[VERTEX, float]] = dd(lambda: dd(None))

        # Initialize 'vertices' as an empty dictionary.
        # This will hold all the vertices of the graph. The keys represent the vertex identifier and the values can hold any data associated with the vertex.
        self.vertices: dict[VERTEX, Optional[VALUE]] = {}

        # Initialize 'cached' as an empty dictionary.
        # This can be used to store computed values for faster access in future computations, acting as a cache.
        self.cached = {}

        # Initialize 'edge_cnt' as 0.
        # This variable keeps track of the total number of edges in the graph.
        self.edge_cnt: int = 0

    # Method to add a vertex to the graph
    def add_vertex(self, index: VERTEX, value: Optional[VALUE] = None):
        # The 'index' parameter represents the identifier for the vertex
        # The 'value' parameter represents the data associated with the vertex. It's optional and defaults to None.
        # The method sets the 'value' as the value for the key 'index' in the 'vertices' dictionary.
        self.vertices[index] = value

    # Method to add a directed edge to the graph
    def add_directed_edge(self, u: VERTEX, v: VERTEX, value: float = 1):
        # The 'u' and 'v' parameters represent the source and destination vertices of the edge.
        # The 'value' parameter represents the weight of the edge. It's optional and defaults to 1.
        # The method sets the 'value' as the value for the key 'v' in the inner dictionary of 'edges' for the key 'u'.
        # This effectively adds an edge from 'u' to 'v' in the 'edges' dictionary.
        # The method then increments the 'edge_cnt' by 1, increasing the total count of edges in the graph.
        self.edges[u][v] = value
        self.edge_cnt += 1

    # Method to add an undirected edge to the graph
    def add_edge(self, u: VERTEX, v: VERTEX, value: float = 1):
        # The 'u' and 'v' parameters represent the vertices to be connected by the edge.
        # The 'value' parameter represents the weight of the edge. It's optional and defaults to 1.
        # The method first adds a directed edge from 'u' to 'v' and then from 'v' to 'u', effectively creating an undirected edge.
        # The 'edge_cnt' is then decremented by 1. This is because the 'add_directed_edge' method increments 'edge_cnt' by 1 each time it's called,
        # so calling it twice actually increments 'edge_cnt' by 2. But since we're adding only one undirected edge, we need to decrement 'edge_cnt' by 1.
        self.add_directed_edge(u, v, value)
        self.add_directed_edge(v, u, value)
        self.edge_cnt -= 1

    # Method to perform Dijkstra's algorithm on the graph
    def djikstra(
        self,
        start: Any,  # The starting vertex for the algorithm
        moves: float = 0,  # The initial number of moves, defaults to 0
        backpack: Backpack[VERTEX] = (),  # A tuple representing the "backpack" of items, defaults to an empty tuple
        can_move_between: CanMoveBetween[
            VALUE
        ] = lambda u, v, backpack: True,  # A function to determine if a move is possible between two vertices, defaults to always returning True
        can_move_to: CanMoveTo[
            VALUE
        ] = lambda u, backpack: True,  # A function to determine if a move is possible to a vertex, defaults to always returning True
        update_backpack: UpdateBackpack[VALUE] = lambda value: set(),  # A function to update the "backpack", defaults to returning an empty set
    ) -> DjikstraSolution[VERTEX, VALUE]:
        # Initialize a stack with the start node, moves, and backpack
        backlog: list[tuple[float, tuple[Any, ...], Any]] = [(moves, backpack, start)]
        # Reset the cache
        self.cached: dict[Any, dict[Any, float]] = dd(lambda: {})
        # While there are nodes in the stack
        while backlog:
            # Pop a node from the stack
            moves, backpack, u = heapq.heappop(backlog)
            # If the node is already in the cache and has fewer moves, skip it
            if backpack in self.cached[u] and self.cached[u][backpack] <= moves:
                continue
            # Add the node to the cache
            self.cached[u][backpack] = moves
            # For each neighbor of the node
            for v in self.edges[u]:
                # If we can move to the neighbor
                if can_move_between(self.vertices[u], self.vertices[v], backpack) and can_move_to(self.vertices[v], backpack):
                    # Add the neighbor to the stack with the updated moves and backpack
                    heapq.heappush(backlog, (moves + self.edges[u][v], self.update_backpack_with_value(backpack, update_backpack(self.vertices[v])), v))
        # Return the cache
        return self.cached

    # Method to update the "backpack" with a new value
    def update_backpack_with_value(
        self, backpack: Backpack[VALUE], value: set[VALUE]
    ) -> tuple[VALUE, ...]:  # The current "backpack" as a tuple  # The new value as a set
        # The method returns a new tuple that represents the updated "backpack".
        # It first converts the "backpack" to a set, then performs a union operation with the new "value" set.
        # The result is then sorted and converted back to a tuple.
        return tuple(sorted(set(backpack) | value))

    # Method to find all vertices in the graph that have a specific value
    def find_all_vertices(self, value: Any) -> Iterator[Any]:  # The value to search for
        # The method iterates over all vertices in the graph.
        # If the value of a vertex equals the specified 'value', it yields that vertex.
        # This method returns a generator that can be used to iterate over all vertices that have the specified value.
        for u in self.vertices:
            if self.vertices[u] == value:
                yield u

    def get_min_for(self, vertex: VERTEX):
        return min(self.cached[vertex].values())

    def get_min_for_value(self, value: VALUE):
        # For each vertex associated with the given value
        # Get the dictionary of vertices and their associated values
        # Then get the minimum value among these values
        # Finally, return the minimum value among all these minimum values
        return min(min(self.cached[u].values()) for u in self.find_all_vertices(value) if len(self.cached[u]) > 0)

    def get_max_for(self, vertex: VERTEX):
        # Get the dictionary of vertices and their associated values for the given vertex
        # Then get the maximum value among these values
        return max(self.cached[vertex].values())

    def get_max_for_value(self, value: VALUE):
        # For each vertex associated with the given value
        # Get the dictionary of vertices and their associated values
        # Then get the maximum value among these values
        # Finally, return the maximum value among all these maximum values
        return max(max(self.cached[u].values()) for u in self.find_all_vertices(value) if len(self.cached[u]) > 0)

    def __repr__(self):
        res = f"Vertices({len(self.vertices)}, Edges({self.edge_cnt}))"
        res += "\n---------------------"
        max_print_vertices = 20
        for i, key in enumerate(self.vertices):
            res += "\n"
            res += f"{key} = {self.vertices[key]}"
            if i + 1 == max_print_vertices:
                break
        res += "\n---------------------"
        max_print_edges = 20
        i = 0
        for u in self.edges:
            for v in self.edges[u]:
                res += "\n"
                res += f"{u} {v in self.edges and u in self.edges[v] and '<' or''}-> {v}"
                i += 1
                if i == max_print_edges:
                    return res
        return res
