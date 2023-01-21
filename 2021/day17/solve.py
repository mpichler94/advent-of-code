from utils.aoc_base import Day
import parse
import math
import itertools
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        data.target_area = parse.parse('target area: x={:d}..{:d}, y={:d}..{:d}', text)

    def compute(self, data):
        v_y = int(-data.target_area[2] - 1)
        return int(v_y * (v_y + 1) / 2)

    def example_answer(self):
        return 45


class PartB(PartA):
    def compute(self, data):
        min_x, max_x, min_y, max_y = self.get_possible_velocities(data.target_area)
        velocities = list(itertools.product(range(min_x, max_x + 1), range(min_y, max_y + 1)))
        return sum(1 for velocity in velocities if self.check_hit(velocity, data.target_area))

    @staticmethod
    def get_possible_velocities(target_area):
        min_x = int(math.ceil((-1 + math.sqrt(1 + 8 * target_area[0])) / 2))
        max_x = int(target_area[1])
        min_y = int(target_area[2])
        max_y = int(-target_area[2] - 1)
        return min_x, max_x, min_y, max_y

    @staticmethod
    def check_hit(velocity, target_area):
        x = 0
        y = 0
        v_x = velocity[0]
        v_y = velocity[1]
        while True:
            x += v_x
            y += v_y
            v_x -= np.sign(v_x)
            v_y -= 1

            if x > target_area[1] or y < target_area[2]:
                return False
            if x >= target_area[0] and y <= target_area[3]:
                return True

    def example_answer(self):
        return 112


Day.do_day(17, 2021, PartA, PartB)
