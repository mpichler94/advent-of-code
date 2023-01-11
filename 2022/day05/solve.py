from utils.aoc_base import Day
import re
from collections import namedtuple


Command = namedtuple('Command', ['count', 'source', 'dest'])


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.commands = []
        towers_finished = False
        data.towers = [[] for _ in range(10)]

        for line in lines:
            if line == '':
                towers_finished = True
                continue

            # read towers
            if not towers_finished:
                if line[1] == '1':
                    continue
                i = 0
                while i * 4 + 1 < len(line):    # 1 5 9
                    crate = line[i * 4 + 1]
                    if crate != ' ':
                        data.towers[i].append(crate)
                    i += 1

            else:
                match = re.search(r'move (\d+) from (\d+) to (\d+)', line)
                data.commands.append(Command(int(match.group(1)), int(match.group(2)) - 1, int(match.group(3)) - 1))

    def compute(self, data):
        for command in data.commands:
            for _ in range(command.count):
                data.towers[command.dest].insert(0, data.towers[command.source].pop(0))

        return self.get_message(data.towers)

    @staticmethod
    def get_message(towers):
        message = ''.join(tower[0] for tower in towers if len(tower) > 0)
        return message.strip()

    def example_answer(self):
        return 'CMZ'


class PartB(PartA):

    def compute(self, data):
        for command in data.commands:
            for i in range(command.count):
                data.towers[command.dest].insert(i, data.towers[command.source].pop(0))

        return self.get_message(data.towers)

    def example_answer(self):
        return 'MCD'


Day.do_day(5, 2022, PartA, PartB)
