import numpy as np
from collections import deque
from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()
        data.numbers = np.zeros(len(lines), dtype=int)
        data.numbers = deque()

        for i, line in enumerate(lines):
            value = int(line)
            data.numbers.append((value, i))
            if value == 0:
                data.zero_idx = i

    def compute(self, data):
        original_numbers = data.numbers.copy()
        self.mix(data, original_numbers)

        i = data.numbers.index((0, data.zero_idx))
        num1 = data.numbers[(i + 1000) % len(data.numbers)][0]
        num2 = data.numbers[(i + 2000) % len(data.numbers)][0]
        num3 = data.numbers[(i + 3000) % len(data.numbers)][0]
        return num1 + num2 + num3

    @staticmethod
    def mix(data, original_numbers):
        for idx in range(len(data.numbers)):
            value = original_numbers[idx]
            num = value[0]
            if num == 0:
                continue
            i = data.numbers.index(value)
            data.numbers.rotate(-i)
            data.numbers.popleft()

            data.numbers.rotate(-num)
            data.numbers.appendleft(value)
            data.numbers.rotate(num)
            data.numbers.rotate(i)
            if num < 0:
                data.numbers.rotate(-1)

    def example_answer(self):
        return 3


class PartB(PartA):
    def config(self, data):
        for i in range(len(data.numbers)):
            data.numbers[i] = (data.numbers[i][0]*811589153, i)

    def compute(self, data):
        original_numbers = data.numbers.copy()
        for _ in range(10):
            self.mix(data, original_numbers)

        i = data.numbers.index((0, data.zero_idx))
        num1 = data.numbers[(i + 1000) % len(data.numbers)][0]
        num2 = data.numbers[(i + 2000) % len(data.numbers)][0]
        num3 = data.numbers[(i + 3000) % len(data.numbers)][0]
        return num1 + num2 + num3

    def example_answer(self):
        return 1623178306


Day.do_day(20, 2022, PartA, PartB)

