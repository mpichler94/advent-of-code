from utils.aoc_base import Day
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        data.positions = []
        data.folds = []
        for line in text.splitlines():
            if line.startswith('fold'):
                fold = line.split('=')
                data.folds.append([fold[0][-1:], int(fold[1])])
            elif line != '':
                pos = line.split(',')
                data.positions.append([int(pos[0]), int(pos[1])])

        data.positions.sort()

    def config(self, data):
        fold = data.folds[0]
        if fold[0] == 'x':
            self.fold_horizontal(data.positions, fold[1])
        else:
            self.fold_vertical(data.positions, fold[1])
        data.positions = self.discard_overlaps(data.positions)

    def compute(self, data):
        return len(data.positions)

    @staticmethod
    def fold_horizontal(points, folding_pos):
        for i in range(len(points)):
            pos = points[i]
            if pos[0] < folding_pos:
                continue
            points[i][0] = 2 * folding_pos - pos[0]

    @staticmethod
    def fold_vertical(points, folding_pos):
        for i in range(len(points)):
            pos = points[i]
            if pos[1] < folding_pos:
                continue
            points[i][1] = 2 * folding_pos - pos[1]

    @staticmethod
    def discard_overlaps(points):
        unique_points = []
        for point in points:
            if point not in unique_points:
                unique_points.append(point)
        return unique_points

    def example_answer(self):
        return 17

    def example_input(self):
        return '''
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
'''


class PartB(PartA):
    def compute(self, data):
        for fold in data.folds:
            if fold[0] == 'x':
                self.fold_horizontal(data.positions, fold[1])
            else:
                self.fold_vertical(data.positions, fold[1])
            data.positions = self.discard_overlaps(data.positions)
        self.print_points(data.positions)

    def print_points(self, points):
        width, height = self.get_dimension(points)
        grid = np.zeros((height, width))
        for point in points:
            grid[point[1], point[0]] = 1

        output = ''
        for line in grid:
            output += '\n' + ''.join([' ' if val == 0 else '#' for val in line])

        print(output)

    @staticmethod
    def get_dimension(points):
        max_x = 0
        max_y = 0
        for p in points:
            if p[0] > max_x:
                max_x = p[0]
            if p[1] > max_y:
                max_y = p[1]

        return max_x + 1, max_y + 1

    def example_answer(self):
        return


Day.do_day(13, 2021, PartA, PartB)
