from functools import reduce
from operator import mul

from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.grid = [[1 if char == "#" else 0 for char in line] for line in text.splitlines()]
        data.slopes = [(3, 1)]

    def compute(self, data):

        total_trees = []
        for slope in data.slopes:
            x = 0
            y = 0
            trees = 0
            while y < len(data.grid):
                if data.grid[y][x] == 1:
                    trees += 1
                x = (x + slope[0]) % len(data.grid[0])
                y += slope[1]
            total_trees.append(trees)

        return reduce(mul, total_trees, 1)

    def example_answer(self):
        return 7


class PartB(PartA):
    def config(self, data):
        data.slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    def example_answer(self):
        return 336


Day.do_day(3, 2020, PartA, PartB)
