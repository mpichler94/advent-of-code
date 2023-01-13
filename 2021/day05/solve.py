import re

from utils.aoc_base import Day
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.v_lines = []    # x, y1, y2
        data.h_lines = []    # y, x1, x2
        data.dd_lines = []   # l, x1, y1  i.e. 3,1 -> 5,3
        data.du_lines = []   # l, x1, y1  i.e. 3,5 -> 5,3

        for line in lines:
            x1, x2, y1, y2 = self.get_points(line)

            if x1 == x2:
                self.add_vline(data.v_lines, x1, y1, y2)

            elif y1 == y2:
                self.add_hline(data.h_lines, y1, x1, x2)

            else:
                self.add_dline(data.dd_lines, data.du_lines, x1, x2, y1, y2)

    @staticmethod
    def get_points(line):
        match = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line)
        x1 = int(match.group(1))
        x2 = int(match.group(3))
        y1 = int(match.group(2))
        y2 = int(match.group(4))
        return x1, x2, y1, y2

    @staticmethod
    def add_vline(v_lines, x, y1, y2):
        if y1 > y2:
            y1, y2 = y2, y1
        v_lines.append([x, y1, y2])

    @staticmethod
    def add_hline(h_lines, y, x1, x2):
        if x1 > x2:
            x1, x2 = x2, x1
        h_lines.append([y, x1, x2])

    @staticmethod
    def add_dline(dd_lines, du_lines, x1, x2, y1, y2):
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        if y1 < y2:
            dd_lines.append([x2 - x1, x1, y1])

        if y1 > y2:
            du_lines.append([x2 - x1, x1, y1])

    def compute(self, data):
        width, height = self.get_field_size(data)
        diagram = np.zeros((width, height))

        for line in data.h_lines:
            for x in range(line[1], line[2] + 1):
                diagram[x, line[0]] += 1
        for line in data.v_lines:
            for y in range(line[1], line[2] + 1):
                diagram[line[0], y] += 1

        num = np.count_nonzero(diagram > 1)
        return num

    @staticmethod
    def get_field_size(data):
        max_x = 0
        max_y = 0
        for line in data.h_lines:
            if line[0] > max_y:
                max_y = line[0]
            if line[2] > max_x:
                max_x = line[2]

        for line in data.v_lines:
            if line[0] > max_x:
                max_x = line[0]
            if line[2] > max_y:
                max_y = line[2]

        return max_x + 1, max_y + 1

    def example_answer(self):
        return 5


class PartB(PartA):
    def compute(self, data):
        width, height = self.get_field_size(data)
        diagram = np.zeros((width, height))

        for line in data.h_lines:
            for x in range(line[1], line[2] + 1):
                diagram[x, line[0]] += 1
        for line in data.v_lines:
            for y in range(line[1], line[2] + 1):
                diagram[line[0], y] += 1
        for line in data.dd_lines:
            for i in range(line[0] + 1):
                diagram[line[1] + i, line[2] + i] += 1
        for line in data.du_lines:
            for i in range(line[0] + 1):
                diagram[line[1] + i, line[2] - i] += 1

        num = np.count_nonzero(diagram > 1)
        return num

    def example_answer(self):
        return 12


Day.do_day(5, 2021, PartA, PartB)
