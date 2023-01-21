import itertools
from functools import reduce
from operator import mul

from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.numbers = [int(number) for number in text.splitlines()]

    def config(self, data):
        data.count = 2

    def compute(self, data):
        for numbers in itertools.permutations(data.numbers, data.count):
            if sum(numbers) == 2020:
                return reduce(mul, numbers, 1)

    def example_answer(self):
        return 514579


class PartB(PartA):
    def config(self, data):
        data.count = 3

    def example_answer(self):
        return 241861950


Day.do_day(1, 2020, PartA, PartB)
