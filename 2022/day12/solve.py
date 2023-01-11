import functools

import nographs

from utils.aoc_base import Day


class PartA(Day):
    def config(self, data):
        data.start = 'S'

    def compute(self, data):
        grid = nographs.Array(data.text.splitlines())
        limits = grid.limits()
        moves = nographs.Position.moves()

        def next_edges(position, _):
            for next_pos in position.neighbors(moves, limits):
                if self.height(grid[next_pos]) <= self.height(grid[position]) + 1:
                    yield next_pos

        start = grid.findall(data.start)
        end = grid.findall('E')[0]

        traversal = nographs.TraversalBreadthFirst(next_edges).start_from(start_vertices=start)
        traversal.go_to(end)

        return traversal.depth

    @staticmethod
    @functools.cache
    def height(char):
        char = 'a' if char == 'S' else char
        char = 'z' if char == 'E' else char
        return ord(char)

    def example_answer(self):
        return 31


class PartB(PartA):
    def config(self, data):
        data.start = 'a'

    def example_answer(self):
        return 29


Day.do_day(12, 2022, PartA, PartB)
