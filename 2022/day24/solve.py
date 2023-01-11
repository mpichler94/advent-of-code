import functools

from utils.aoc_base import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.width = len(lines[0]) - 2
        data.height = len(lines) - 2

        for i, c in enumerate(lines[0]):
            if c == '.':
                data.start = i-1
                break
        for i, c in enumerate(lines[-1]):
            if c == '.':
                data.goal = i-1
                break

        data.blizzards = []
        for y in range(len(lines) - 2):
            line = lines[y+1]
            for x, c in enumerate(line):
                if c == '^':
                    data.blizzards.append(((0, -1), (x-1, y)))
                if c == 'v':
                    data.blizzards.append(((0, 1), (x-1, y)))
                if c == '<':
                    data.blizzards.append(((-1, 0), (x-1, y)))
                if c == '>':
                    data.blizzards.append(((1, 0), (x-1, y)))

    def config(self, data):

        def blizzard_generator():
            count = 1
            while True:
                blizzard_locations = set()
                for blizzard in data.blizzards:
                    (dx, dy), (x, y) = blizzard
                    x = (x + dx * count) % data.width
                    y = (y + dy * count) % data.height
                    blizzard_locations.add((x, y))

                count += 1
                yield blizzard_locations

        blizzard_iter = iter(blizzard_generator())

        @functools.cache
        def blizzards(time):
            return next(blizzard_iter)

        def next_edges(state, _):
            x, y, time = state
            next_time = time + 1
            blizzard_locations = blizzards(next_time)
            for next_x, next_y in nog.Position((x, y)).neighbors(nog.Position.moves(zero_move=True)):
                if 0 <= next_x < data.width and 0 <= next_y < data.height and (next_x, next_y) not in blizzard_locations:
                    yield (next_x, next_y, next_time), 1
                if next_x == data.start and next_y == -1:
                    yield(next_x, next_y, next_time), 1
                if next_x == data.goal and next_y == data.height:
                    yield(next_x, next_y, next_time), 1

        data.traversal = nog.TraversalAStar(next_edges)

    @staticmethod
    def heuristic(goal):
        def distance(state):
            x, y, time = state
            return nog.Position((x, y)).manhattan_distance(nog.Position(goal))
        return distance

    def compute(self, data):
        for state in data.traversal.start_from(self.heuristic((data.goal, data.height)), (data.start, -1, 0)):
            x, y, time = state
            if y == data.height and x == data.goal:
                return data.traversal.depth

    def example_input(self):
        return '''
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.# '''

    def example_answer(self):
        return 18


class PartB(PartA):
    def compute(self, data):
        paths = [((data.start, -1), (data.goal, data.height)), ((data.goal, data.height), (data.start, -1)), ((data.start, -1), (data.goal, data.height))]
        total_time = 0
        for start, end in paths:
            for state in data.traversal.start_from(self.heuristic(end), (start[0], start[1], total_time)):
                x, y, time = state
                if y == end[1] and x == end[0]:
                    total_time += data.traversal.depth
                    break

        return total_time

    def example_answer(self):
        return 54


Day.do_day(24, 2022, PartA, PartB)
