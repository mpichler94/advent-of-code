import re

from utils.aoc_base import Day


class Monkey:
    def __init__(self, name, inputs, operation):
        self.name = name
        self.inputs = inputs
        self.operation = operation

    def get_result(self, monkeys):
        for monkey in self.inputs:
            locals()[monkey] = monkeys[monkey].get_result(monkeys)
        return eval(self.operation)

    @staticmethod
    def from_string(str):
        match = re.match(r'(.*?): (.*)', str)
        name = match.group(1)
        op = match.group(2)
        parts = op.split(' ')
        inputs = []
        if len(parts) > 1:
            inputs.append(parts[0])
            inputs.append(parts[2])

        return Monkey(name, inputs, op)


class PartA(Day):
    def parse(self, text: str, data):
        lines = text.splitlines()
        data.monkeys = {}
        for line in lines:
            monkey = Monkey.from_string(line)
            data.monkeys[monkey.name] = monkey

    def compute(self, data):
        value = data.monkeys['root'].get_result(data.monkeys)

        return int(value)

    def example_answer(self):
        return 152


class PartB(PartA):
    def compute(self, data):
        todo = ['humn']
        new_monkeys = dict(data.monkeys)
        while len(todo) > 0:
            name = todo.pop(0)
            for monkey in data.monkeys.values():
                if name in monkey.inputs:
                    other_monkey = monkey.inputs[1] if name == monkey.inputs[0] else monkey.inputs[0]
                    if monkey.name == 'root':
                        new_monkeys[name] = Monkey(name, [], str(data.monkeys[other_monkey].get_result(data.monkeys)))
                        continue

                    op = self.reorder(monkey, name)
                    inputs = [monkey.name, other_monkey]
                    new_monkeys[name] = Monkey(name, inputs, op)
                    todo.append(monkey.name)

        return int(new_monkeys['humn'].get_result(new_monkeys))

    @staticmethod
    def reorder(monkey, target):
        parts = monkey.operation.split(' ')
        left = parts[0]
        right = parts[2]
        op = parts[1]
        other = right if target == left else left

        if op == '+':
            return f'{monkey.name} - {other}'
        elif op == '-':
            if target == left:
                return f'{monkey.name} + {right}'
            return f'{left} - {monkey.name}'
        elif op == '*':
            return f'{monkey.name} / {other}'
        elif op == '/':
            if target == left:
                return f'{monkey.name} * {right}'
            return f'{left} / {monkey.name}'

        raise RuntimeError('Cannot reorder operation')

    def example_answer(self):
        return 301


Day.do_day(21, 2022, PartA, PartB)
