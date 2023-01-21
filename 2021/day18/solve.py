from utils.aoc_base import Day
import itertools
import re
import math


class PartA(Day):
    def parse(self, text, data):
        data.numbers = text.splitlines()

    def compute(self, data):
        number = self.add(data.numbers)
        return self.magnitude(number)

    def add(self, numbers):
        left = numbers[0]
        for i in range(1, len(numbers)):
            left = self.reduce(f'[{left},{numbers[i]}]')
        return left

    def reduce(self, number):
        reduced = self.explode(number)
        if reduced != number:
            return self.reduce(reduced)

        reduced = self.split(number)
        if reduced != number:
            return self.reduce(reduced)

        return reduced

    @staticmethod
    def explode(number):
        i = 0
        while i < len(number):
            pair = re.search(r'\[(\d+),(\d+)\]', number[i:])
            if pair is None:
                break
            depth = number[:pair.start() + i].count('[')
            depth -= number[:pair.start() + i].count(']')
            if depth >= 4:
                l_add = int(pair[1])
                r_add = int(pair[2])
                left_part = number[pair.start() + i - 1::-1]
                right_part = number[pair.end() + i:]
                left = re.search(r'\d+', left_part)
                if left:
                    left_part = f'{left_part[:left.start()]}{str(l_add + int(left[0][::-1]))[::-1]}{left_part[left.end():]}'
                right = re.search(r'\d+', number[pair.end() + i:])
                if right:
                    right_part = f'{right_part[:right.start()]}{r_add + int(right[0])}{right_part[right.end():]}'
                number = f'{left_part[::-1]}0{right_part}'
                break

            i += pair.end()
        return number

    @staticmethod
    def split(number):
        regular_num = re.search(r'\d\d', number)
        if regular_num is None:
            return number

        left = int(regular_num[0]) // 2
        right = math.ceil(int(regular_num[0]) / 2)
        number = f'{number[:regular_num.start()]}[{left},{right}]{number[regular_num.end():]}'

        return number

    @staticmethod
    def magnitude(number):
        while True:
            pair = re.search(r'\[(\d+),(\d+)\]', number)
            if pair is None:
                return int(number)
            mag = 3 * int(pair[1]) + 2 * int(pair[2])
            number = f'{number[:pair.start()]}{mag}{number[pair.end():]}'

    def example_answer(self):
        return 4230


class PartB(PartA):
    def compute(self, data):
        magnitudes = []
        for pair in itertools.permutations(data.numbers, 2):
            number = self.add(pair)
            magnitudes.append(self.magnitude(number))
        return max(magnitudes)

    def example_answer(self):
        return 4647


Day.do_day(18, 2021, PartA, PartB)
