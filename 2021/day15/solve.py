import nographs
from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.cave = nographs.Array([[int(weight) for weight in line] for line in text.splitlines()])
        data.limits = data.cave.limits()
        data.moves = nographs.Position.moves()
        data.start = nographs.Position.at(0, 0)
        data.end = nographs.Position.at(data.limits[0][1] - 1, data.limits[1][1] - 1)

    def config(self, data):
        def get_risk(pos):
            return data.cave[pos]
        data.risk = get_risk

    def compute(self, data):
        def next_edges(pos, _):
            for neighbor in pos.neighbors(data.moves, data.limits):
                yield neighbor, data.risk(neighbor)

        def heuristic(pos):
            return pos.manhattan_distance(data.end)

        traversal = nographs.TraversalAStar(next_edges)
        traversal.start_from(heuristic, data.start).go_to(data.end)
        return traversal.distances[data.end]

    def example_answer(self):
        return 40


class PartB(PartA):
    def config(self, data):
        def get_risk(pos):
            block_x, x = divmod(pos[0], width)
            block_y, y = divmod(pos[1], height)
            return (data.cave[(x, y)] + block_x + block_y - 1) % 9 + 1
        width = data.limits[0][1]
        height = data.limits[1][1]
        data.risk = get_risk
        data.limits = [(0, width * 5), (0, height * 5)]
        data.end = nographs.Position.at(data.limits[0][1] - 1, data.limits[1][1] - 1)

    def example_answer(self):
        return 315


Day.do_day(15, 2021, PartA, PartB)
