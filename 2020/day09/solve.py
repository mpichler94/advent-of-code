from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.numbers = [int(num) for num in text.splitlines()]

    def compute(self, data):
        return data.numbers[self.find_invalid(data.numbers)]

    @staticmethod
    def find_invalid(numbers):
        length = 25 if len(numbers) >= 25 else 5
        for i in range(length, len(numbers)):
            preamble = numbers[i - length : i]
            preamble.sort()
            l = 0
            r = length - 1
            while l < r:
                diff = numbers[i] - preamble[l] - preamble[r]
                if diff == 0:
                    break
                if diff < 0:
                    r -= 1
                else:
                    l += 1

            if l >= r:
                break
        return i

    def example_answer(self):
        return 127


class PartB(PartA):
    def compute(self, data):
        i = self.find_invalid(data.numbers)
        num = data.numbers[i]

        for i in range(i):
            j = i + 2
            while sum(data.numbers[i:j]) < num and j <= len(data.numbers):
                j += 1
            if num == sum(data.numbers[i:j]):
                target = data.numbers[i:j]
                target.sort()
                return target[0] + target[-1]

    def example_answer(self):
        return 62


Day.do_day(9, 2020, PartA, PartB)
