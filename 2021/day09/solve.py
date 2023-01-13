import nographs

from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()
        data.heights = nographs.Array([[int(char) for char in line] for line in lines])
        data.limits = data.heights.limits()
        data.moves = nographs.Position.moves()

    def config(self, data):
        data.low_points = self.get_low_points(data)

    def compute(self, data):
        return sum(data.heights[p] + 1 for p in data.low_points)     # risk level is height + 1

    @staticmethod
    def get_low_points(data):
        low_points = []
        for x in range(data.limits[0][1]):
            for y in range(data.limits[1][1]):
                pos = nographs.Position.at(x, y)
                neighbor_heights = [data.heights[p] for p in pos.neighbors(data.moves, data.limits)]
                if all(data.heights[pos] < h for h in neighbor_heights):
                    low_points.append(pos)
        return low_points

    def example_answer(self):
        return 15


class PartB(PartA):

    def compute(self, data):
        basin_sizes = [self.get_basin_size(data, low_point) for low_point in data.low_points]
        basin_sizes.sort()
        return basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]

    @staticmethod
    def get_basin_size(data, pos):
        def next_edges(pos, _):
            for n in pos.neighbors(data.moves, data.limits):
                if data.heights[pos] < data.heights[n] < 9:
                    yield n

        traversal = nographs.TraversalBreadthFirst(next_edges)
        return len(set(traversal.start_from(pos, already_visited=set()))) + 1

    def example_answer(self):
        return 1134


Day.do_day(9, 2021, PartA, PartB)
