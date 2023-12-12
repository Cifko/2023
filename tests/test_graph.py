import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers.graph import Graph


class TestAdd(unittest.TestCase):
    def test_1(self):
        g = Graph[str, int]()
        g.add_vertex("a", "a")
        g.add_vertex("b", "b")
        g.add_vertex("c", "c")
        g.add_edge("a", "b", 1)
        g.add_edge("b", "c", 5)
        g.add_edge("c", "a", 1)
        s = g.djikstra("a", update_backpack=lambda v: {v})
        print(g.get_max_for("a"))
        print(g.get_max_for_value(4))
        print(s)


# This allows the test to be run
if __name__ == "__main__":
    unittest.main()
