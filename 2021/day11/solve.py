import itertools

from utils.aoc_base import Day
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()
        data.energy_levels = np.zeros((10, 10))

        for x, y in itertools.product(range(10), repeat=2):
            data.energy_levels[x, y] = int(lines[y][x])

    def compute(self, data):
        flashes = 0
        for _ in range(100):
            data.energy_levels, step_flashes = self.step(data.energy_levels)
            flashes += step_flashes
        return flashes

    def step(self, energy_levels):
        energy_levels += 1
        self.process_flashes(energy_levels)
        step_flashes = np.sum(np.where(energy_levels > 9, 1, 0))
        energy_levels = np.where(energy_levels > 9, 0, energy_levels)

        return energy_levels, step_flashes

    def process_flashes(self, energy_levels):
        flashed = True
        flashed_positions = []
        while flashed:
            flashed = False
            for x, y in itertools.product(range(10), repeat=2):
                if energy_levels[x, y] > 9 and [x, y] not in flashed_positions:
                    flashed = True
                    self.flash(energy_levels, x, y)
                    flashed_positions.append([x, y])

    @staticmethod
    def flash(energy_levels, center_x, center_y):
        for y in range(max(0, center_y - 1), min(center_y + 1, 9) + 1):
            for x in range(max(0, center_x - 1), min(center_x + 1, 9) + 1):
                if x != center_x or y != center_y:
                    energy_levels[x, y] += 1

    def example_answer(self):
        return 1656


class PartB(PartA):
    def compute(self, data):
        flashes = 0
        steps = 1
        while flashes != 100:
            data.energy_levels, flashes = self.step(data.energy_levels)
            steps += 1

        return steps - 1

    def example_answer(self):
        return 195


Day.do_day(11, 2021, PartA, PartB)
