import math

from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.instructions = [(line[0], int(line[1:])) for line in text.splitlines()]

    def compute(self, data):
        dir = 0
        x = 0
        y = 0
        for cmd, count in data.instructions:
            match cmd:
                case "N":
                    y -= count
                case "S":
                    y += count
                case "E":
                    x += count
                case "W":
                    x -= count
                case "L":
                    dir -= count
                case "R":
                    dir += count
                case "F":
                    x += int(math.cos(dir * math.pi / 180) * count)
                    y += int(math.sin(dir * math.pi / 180) * count)

        return abs(x) + abs(y)

    def example_answer(self):
        return 25


class PartB(PartA):
    def compute(self, data):
        w_x = 10
        w_y = -1
        x = 0
        y = 0

        for cmd, count in data.instructions:
            match cmd:
                case "N":
                    w_y -= count
                case "S":
                    w_y += count
                case "E":
                    w_x += count
                case "W":
                    w_x -= count
                case "L":
                    w_x, w_y = self.rotate(-count, (x, y), (w_x, w_y))
                case "R":
                    w_x, w_y = self.rotate(count, (x, y), (w_x, w_y))
                case "F":
                    d_x = (w_x - x) * count
                    d_y = (w_y - y) * count
                    x += d_x
                    w_x += d_x
                    y += d_y
                    w_y += d_y

        return abs(x) + abs(y)

    @staticmethod
    def rotate(angle, center, pos):
        radians = angle * math.pi / 180
        new_x = int(center[0] + (pos[0] - center[0]) * math.cos(radians) - (pos[1] - center[1]) * math.sin(radians))
        new_y = int(center[1] + (pos[0] - center[0]) * math.sin(radians) + (pos[1] - center[1]) * math.cos(radians))
        return new_x, new_y

    def example_answer(self):
        return 286


Day.do_day(12, 2020, PartA, PartB)
