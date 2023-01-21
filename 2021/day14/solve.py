from utils.aoc_base import Day
from functools import lru_cache
from collections import Counter


class PartA(Day):
    def parse(self, text, data):
        data.template, rules = text.split('\n\n')
        data.rules = dict(line.split(' -> ') for line in rules.splitlines())

    def config(self, data):
        data.num_steps = 10

    def compute(self, data):
        counter = Counter(self.process_polymer(data.template, data.rules, data.num_steps))
        return max(counter.values()) - min(counter.values())

    @staticmethod
    def process_polymer(template, rules, iterations):
        @lru_cache(maxsize=None)    # caches inputs and outputs to skip repeating function calls
        def replace_and_count(pair, iteration):
            if iteration >= iterations:
                return Counter()
            pair1 = pair[0] + rules[pair]
            pair2 = rules[pair] + pair[1]
            counter = Counter(list(rules[pair]))
            counter.update(replace_and_count(pair1, iteration + 1))
            counter.update(replace_and_count(pair2, iteration + 1))
            return counter

        counter = Counter(list(template))
        for i in range(len(template) - 1):
            counter.update(replace_and_count(template[i:i + 2], 0))
        return counter

    def example_answer(self):
        return 1588


class PartB(PartA):
    def config(self, data):
        data.num_steps = 40

    def example_answer(self):
        return 2188189693529


Day.do_day(14, 2021, PartA, PartB)
