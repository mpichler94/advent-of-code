from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        groups = text.split("\n\n")
        data.groups = [row.splitlines() for row in groups]

    def compute(self, data):
        return sum(self.get_yes_count(group) for group in data.groups)

    def get_yes_count(self, group):
        questions = set()
        for row in group:
            questions.update(row)
        return len(questions)

    def example_answer(self):
        return 11

    def example_input(self):
        return """
abc

a
b
c

ab
ac

a
a
a
a

b
"""


class PartB(PartA):
    def get_yes_count(self, group):
        answers = set(group[0])
        for row in group:
            answers = answers.intersection(set(row))
        return len(answers)

    def example_answer(self):
        return 6


Day.do_day(6, 2020, PartA, PartB)
