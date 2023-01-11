from utils.aoc_base import Day
import re
import math


class Monkey:
    def __init__(self, items, operation, divisor, true_num, false_num, relief=True):
        self.fac = 0
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.true_num = true_num
        self.false_num = false_num
        self.count = 0
        self.relief = relief

    def add_item(self, item):
        self.items.append(item)

    def round(self, monkeys):
        self.fac = math.prod(monkey.divisor for monkey in monkeys)
        while len(self.items) > 0:
            item = self.items.pop(0)
            self.process_item(monkeys, item)

    def process_item(self, monkeys, item):
        self.count += 1
        old = item
        exec(self.operation)
        item = locals()['new']
        if self.relief:
            item = item // 3
        else:
            item = item % self.fac
        if item % self.divisor == 0:
            monkeys[self.true_num].add_item(item)
        else:
            monkeys[self.false_num].add_item(item)


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.monkeys = []
        for i in range(0, len(lines), 7):
            items = [int(item) for item in lines[i+1][18:].split(', ')]
            op = lines[i+2].replace('Operation: ', '').strip()
            match = re.match(r'.*?(\d+)', lines[i+3])
            divisor = int(match.group(1))
            match = re.match(r'.*(\d+)', lines[i+4])
            true_num = int(match.group(1))
            match = re.match(r'.*(\d+)', lines[i+5])
            false_num = int(match.group(1))
            data.monkeys.append(Monkey(items, op, divisor, true_num, false_num))

    def config(self, data):
        data.num_rounds = 20

    def compute(self, data):
        for _ in range(data.num_rounds):
            for monkey in data.monkeys:
                monkey.round(data.monkeys)

        counts = []
        for i in range(len(data.monkeys)):
            counts.append(data.monkeys[i].count)

        counts.sort()
        return counts[-1] * counts[-2]

    def example_answer(self):
        return 10605


class PartB(PartA):
    def config(self, data):
        data.num_rounds = 10000
        for monkey in data.monkeys:
            monkey.relief = False

    def example_answer(self):
        return 2713310158


Day.do_day(11, 2022, PartA, PartB)
