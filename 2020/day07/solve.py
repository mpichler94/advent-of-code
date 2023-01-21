import re

from utils.aoc_base import Day


class Bag:
    def __init__(self, name, contents):
        self.name = name
        self.contents = contents  # list of tuples(count, Bag)

    def init(self, bags):
        self.contents = [(count, bags[bag]) for count, bag in self.contents]

    def contains(self, name):
        for _, bag in self.contents:
            if bag.name == name:
                return True
            if bag.contains(name):
                return True

        return False

    def count_containing(self):
        return 1 + sum(count * bag.count_containing() for count, bag in self.contents)

    @classmethod
    def from_text(cls, text):
        name, contents = text.split(" bags contain ")
        parts = contents.split(", ")
        bags = []
        for part in parts:
            part = part.replace(".", "")
            if part == "no other bags":
                break
            match = re.match(r"(\d+) (.*) bags?", part)
            bags.append((int(match.group(1)), match.group(2)))
        return cls(name, bags)

    def __repr__(self):
        if len(self.contents) == 0:
            content = "no other bags"
        else:
            content = "".join(f"{count} {name} bag" for count, name in self.contents)
        return f"{self.name} bag contain {content}."


class PartA(Day):
    def parse(self, text, data):
        data.bags = {}
        for line in text.splitlines():
            bag = Bag.from_text(line)
            data.bags[bag.name] = bag

        for bag in data.bags.values():
            bag.init(data.bags)

    def compute(self, data):
        count = 0
        for bag in data.bags.values():
            if bag.contains("shiny gold"):
                count += 1
        return count

    def example_answer(self):
        return 4


class PartB(PartA):
    def compute(self, data):
        return data.bags["shiny gold"].count_containing() - 1

    def example_answer(self):
        return 32


Day.do_day(7, 2020, PartA, PartB)
