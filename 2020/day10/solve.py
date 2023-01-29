from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.numbers = [int(num) for num in text.splitlines()]
        data.numbers.sort()
        data.numbers.insert(0, 0)
        data.numbers.append(data.numbers[-1] + 3)
        data.diff = [j - i for i, j in zip(data.numbers[:-1], data.numbers[1:])]

    def compute(self, data):
        return data.diff.count(1) * data.diff.count(3)

    def example_answer(self):
        return 35


class PartB(PartA):
    def compute(self, data):
        opt = []
        for i in range(len(data.diff) - 1):
            opt.append(1 if data.diff[i] + data.diff[i + 1] <= 3 else 0)

        arrangements = 1
        for i, o in enumerate(opt):
            if o == 1 and i > 1 and opt[i - 1] == 1 and opt[i - 2] == 1:
                arrangements *= 1.75
            elif o == 1:
                arrangements *= 2
        return int(arrangements)

    def example_answer(self):
        return 8


Day.do_day(10, 2020, PartA, PartB)
