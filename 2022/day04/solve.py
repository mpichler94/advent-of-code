from utils.aoc_base import Day
import re


class PartA(Day):
    def parse(self, text, data):
        data.pairs = [line for line in text.splitlines()]

    def compute(self, data):
        sum = 0
        for pair in data.pairs:
            section1, section2 = self.get_sections(pair)

            if section1.intersection(section2) == section1 or section2.intersection(section1) == section2:
                sum += 1

        return sum

    @staticmethod
    def get_sections(pair):
        match = re.search("^(\d+)-(\d+),(\d+)-(\d+)", pair)

        startS1 = int(match.group(1))
        startS2 = int(match.group(3))
        endS1 = int(match.group(2))
        endS2 = int(match.group(4))

        section1 = set(range(startS1, endS1+1))
        section2 = set(range(startS2, endS2 + 1))

        return section1, section2

    def example_answer(self):
        return 2


class PartB(PartA):
    def compute(self, data):
        sum = 0
        for pair in data.pairs:
            section1, section2 = self.get_sections(pair)

            overlap = section1.intersection(section2)
            if len(overlap) > 0:
                sum += 1

        return sum

    def example_answer(self):
        return 4


Day.do_day(4, 2022, PartA, PartB)
