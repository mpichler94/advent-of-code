from utils.aoc_base import Day
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        data.numbers = np.fromstring(text, dtype=int, sep='\n')

    def compute(self, data):
        count = self.count_increases(data.numbers)
        return count

    @staticmethod
    def count_increases(data):
        diff = np.diff(data)
        count = np.count_nonzero(diff > 0)
        return count

    def example_answer(self):
        return 7


class PartB(PartA):
    def config(self, data):
        data.numbers = self.create_mean(data.numbers)

    @staticmethod
    def create_mean(data):
        ret = np.convolve(data, np.ones(3))
        return ret[2:]

    def example_answer(self):
        return 5


Day.do_day(1, 2021, PartA, PartB)
