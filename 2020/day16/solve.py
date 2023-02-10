import re

from utils.aoc_base import Day


class Rule:
    def __init__(self, name, ranges):
        self.name = name
        self.min1 = ranges[0][0]
        self.min2 = ranges[1][0]
        self.max1 = ranges[0][1]
        self.max2 = ranges[1][1]

    def check_field(self, value):
        if self.min1 <= value <= self.max1:
            return True
        if self.min2 <= value <= self.max2:
            return True
        return False

    def __repr__(self):
        return f"{self.name}: {self.min1}-{self.max1} or {self.min2}-{self.max2}"


class PartA(Day):
    def parse(self, text, data):
        rules, ticket, tickets = text.split("\n\n")

        data.rules = []
        for rule in rules.splitlines():
            match = re.match(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)", rule)
            data.rules.append(
                Rule(
                    match.group(1),
                    [(int(match.group(2)), int(match.group(3))), (int(match.group(4)), int(match.group(5)))],
                )
            )

        data.my_ticket = [int(num) for num in ticket.splitlines()[1].split(",")]

        data.tickets = []
        for line in tickets.splitlines()[1:]:
            data.tickets.append([int(num) for num in line.split(",")])

    def compute(self, data):
        error_rate = 0
        for ticket in data.tickets:
            for value in ticket:
                if any(rule.check_field(value) for rule in data.rules):
                    continue
                error_rate += value

        return error_rate

    def example_answer(self):
        return 71

    def example_input(self):
        return """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12        
"""


class PartB(PartA):
    def compute(self, data):
        data.tickets = self.remove_invalid_tickets(data.tickets, data.rules)

        possibilities = self.get_possibilities(data.tickets, data.rules)

        possibilities = self.demultiply_possibilities(possibilities)

        targets = [rule.name for rule in data.rules if rule.name.startswith("departure")]
        indices = []
        for target in targets:
            for i in range(len(possibilities)):
                if target in possibilities[i]:
                    indices.append(i)

        value = 1
        for target in indices:
            value *= data.my_ticket[target]

        return value

    @staticmethod
    def remove_invalid_tickets(tickets, rules):
        rem_tickets = []
        for ticket in tickets:
            for value in ticket:
                if any(rule.check_field(value) for rule in rules):
                    continue
                rem_tickets.append(ticket)
        for t in rem_tickets:
            tickets.remove(t)
        return tickets

    @staticmethod
    def get_possibilities(tickets, rules):
        possibilities = [[rule.name for rule in rules] for _ in range(len(tickets[0]))]

        for ticket in tickets:
            for rule in rules:
                for i, value in enumerate(ticket):
                    if not rule.check_field(value) and rule.name in possibilities[i]:
                        possibilities[i].remove(rule.name)

        return possibilities

    @staticmethod
    def demultiply_possibilities(possibilities):
        while True:
            finished = True
            for i in range(len(possibilities)):
                if len(possibilities[i]) == 1:
                    value = possibilities[i][0]
                    for j in range(len(possibilities)):
                        if i != j and value in possibilities[j]:
                            possibilities[j].remove(value)
                elif len(possibilities[i]) > 1:
                    finished = False

            if finished:
                break
        return possibilities

    def example_input(self):
        return """
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9        
"""

    def example_answer(self):
        return 1


Day.do_day(16, 2020, PartA, PartB)
