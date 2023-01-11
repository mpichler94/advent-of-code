from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.rounds = [line.replace(' ', '') for line in lines]

    def config(self, data):
        data.table = {
            'AX': 4,
            'AY': 8,
            'AZ': 3,
            'BX': 1,
            'BY': 5,
            'BZ': 9,
            'CX': 7,
            'CY': 2,
            'CZ': 6
        }

    def compute(self, data):
        return sum(data.table[i] for i in data.rounds)

    def example_answer(self):
        return 15


class PartB(PartA):
    def config(self, data):
        data.table = {
            'AX': 3,
            'AY': 4,
            'AZ': 8,
            'BX': 1,
            'BY': 5,
            'BZ': 9,
            'CX': 2,
            'CY': 6,
            'CZ': 7
        }

    def example_answer(self):
        return 12


Day.do_day(2, 2022, PartA, PartB)
