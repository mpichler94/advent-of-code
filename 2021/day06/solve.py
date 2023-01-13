from utils.aoc_base import Day
import numpy as np


class PartA(Day):
    def parse(self, text, data):

        data.fish = np.zeros(9, dtype=np.longlong)
        for a_fish in text.split(','):
            days = int(a_fish)
            data.fish[days] += 1

    def config(self, data):
        data.num_days = 80

    def compute(self, data):
        for _ in range(data.num_days):
            self.simulate_day(data.fish)
        return int(np.sum(data.fish))

    @staticmethod
    def simulate_day(fish):
        new_fish = fish[0]
        fish[0] = 0
        for i in range(1, len(fish)):
            fish[i - 1] += fish[i]
            fish[i] = 0

        fish[8] += new_fish
        fish[6] += new_fish

    def example_answer(self):
        return 5934


class PartB(PartA):
    def config(self, data):
        data.num_days = 256

    def example_answer(self):
        return 26984457539


Day.do_day(6, 2021, PartA, PartB)
