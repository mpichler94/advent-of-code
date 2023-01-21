import re
from collections import namedtuple

from utils.aoc_base import Day

Password = namedtuple("Password", ["min", "max", "char", "password"])


class PartA(Day):
    def parse(self, text, data):
        data.passwords = []
        for line in text.splitlines():
            match = re.match(r"(\d+)-(\d+) (.): (.*)", line)
            data.passwords.append(
                Password(
                    int(match.group(1)),
                    int(match.group(2)),
                    match.group(3),
                    match.group(4),
                )
            )

    def compute(self, data):
        correct = 0
        for password in data.passwords:
            if password.min <= password.password.count(password.char) <= password.max:
                correct += 1

        return correct

    def example_answer(self):
        return 2


class PartB(PartA):
    def compute(self, data):
        count = 0
        for pw in data.passwords:
            if pw.password[pw.min - 1] == pw.char and pw.password[pw.max - 1] != pw.char:
                count += 1
                continue
            if pw.password[pw.max - 1] == pw.char and pw.password[pw.min - 1] != pw.char:
                count += 1
        return count

    def example_answer(self):
        return 1


Day.do_day(2, 2020, PartA, PartB)
