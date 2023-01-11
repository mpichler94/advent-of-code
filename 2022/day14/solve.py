from utils.aoc_base import Day
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()
        w = 1000
        h = 500

        data.void_y = 0
        data.grid = np.zeros((h, w), dtype=int)
        for i in range(0, len(lines), 1):
            line = lines[i].strip()
            prev = None
            for pos in line.split(' -> '):
                tmp = pos.split(',')
                xy = [int(tmp[1]), int(tmp[0])]
                data.void_y = max(data.void_y, xy[0]+1)
                if prev is None:
                    prev = xy
                    continue

                if xy[0] == prev[0]:
                    start = prev[1]
                    end = xy[1]
                    for y in range(min(start, end), max(start, end)+1):
                        data.grid[xy[0], y] = 1

                elif xy[1] == prev[1]:
                    start = prev[0]
                    end = xy[0]
                    for x in range(min(start, end), max(start, end)+1):
                        data.grid[x, xy[1]] = 1

                prev = xy

    def compute(self, data):
        count = 0
        while True:
            count += 1
            reached_void = self.put_sand(data.grid, data.void_y)
            if reached_void:
                return count - 1

    @staticmethod
    def put_sand(grid, void_y):
        s_x = 500
        s_y = 0

        while True:
            if s_y >= void_y:
                grid[s_y, s_x] = 2
                return True

            if grid[s_y+1, s_x] == 0:
                s_y += 1
            elif grid[s_y+1, s_x-1] == 0:
                s_x -= 1
                s_y += 1
            elif grid[s_y+1, s_x+1] == 0:
                s_x += 1
                s_y += 1
            else:
                break

        if s_y == 0 and s_x == 500:
            return True

        grid[s_y, s_x] = 2
        if s_y >= void_y:
            return True

        return False

    def example_answer(self):
        return 24


class PartB(PartA):
    def config(self, data):
        for x in range(data.grid.shape[1]):
            data.grid[data.void_y+1, x] = 1
        data.void_y = 500

    def compute(self, data):
        return PartA.compute(self, data) + 1

    def example_answer(self):
        return 93


Day.do_day(14, 2022, PartA, PartB)