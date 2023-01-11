from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.sums = []
        calories = 0

        for line in lines:
            if line == '':
                data.sums.append(calories)
                calories = 0
                continue

            calories += int(line)
        data.sums.append(calories)

    def compute(self, data):
        return max(data.sums)

    def example_answer(self):
        return 24000


class PartB(PartA):
    def compute(self, data):
        sums = sorted(data.sums)
        return sums[-1] + sums[-2] + sums[-3]

    def example_answer(self):
        return 45000


Day.do_day(1, 2022, PartA, PartB)
