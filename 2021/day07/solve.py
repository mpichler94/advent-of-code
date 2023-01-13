from utils.aoc_base import Day
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        data.crabs = np.fromstring(text, dtype=int, sep=',')

    def config(self, data):
        def cost_a(pos, crabs):
            return np.sum(np.abs(pos - crabs))
        data.cost = cost_a

    @staticmethod
    def all_costs(crabs, cost_function):
        max_pos = np.max(crabs)
        costs = np.zeros(max_pos + 1)
        for i in range(max_pos + 1):
            costs[i] = cost_function(i, crabs)

        return costs

    def compute(self, data):
        costs = self.all_costs(data.crabs, data.cost)
        idx = np.argmin(costs)
        return int(costs[idx])

    def example_answer(self):
        return 37


class PartB(PartA):
    def config(self, data):
        def cost_b(pos, crabs):
            diff = np.abs(pos - crabs)
            return np.sum(diff * (diff + 1) / 2)
        data.cost = cost_b

    def example_answer(self):
        return 168


Day.do_day(7, 2021, PartA, PartB)
