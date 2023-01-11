from utils.aoc_base import Day
from collections import namedtuple
import numpy as np

Command = namedtuple('Command', ['direction', 'count'])


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.commands = []
        for line in lines:
            line = line.replace('\n', '')
            parts = line.split()
            data.commands.append(Command(parts[0], int(parts[1])))

    def config(self, data):
        data.pos = [[0, 0] for _ in range(2)]

    def compute(self, data):
        positions = []
        count = 0

        for command in data.commands:
            for _ in range(command.count):
                pos = self.move(command.direction, data.pos)
                p = f'{pos[-1][0]}.{pos[-1][1]}'
                if p not in positions:
                    count += 1
                    positions.append(p)

        return count

    def move(self, direction, pos):
        pos[0][0], pos[0][1] = self.move_head(direction, pos[0][0], pos[0][1])

        for i in range(1, len(pos)):
            pos[i][0], pos[i][1] = self.move_tail(pos[i-1][0], pos[i-1][1], pos[i][0], pos[i][1])

        return pos

    @staticmethod
    def move_head(direction, hx, hy):
        if direction == 'U':
            hy += 1
        elif direction == 'D':
            hy -= 1
        elif direction == 'R':
            hx += 1
        elif direction == 'L':
            hx -= 1
        return hx, hy

    @staticmethod
    def move_tail(hx, hy, tx, ty):
        if abs(hx - tx) > 1:
            tx += np.sign(hx - tx)
            if hy != ty:
                ty += np.sign(hy - ty)
        elif abs(hy - ty) > 1:
            ty += np.sign(hy - ty)
            if hx != tx:
                tx += np.sign(hx - tx)
        return tx, ty

    def example_answer(self):
        return 13

    def example_input(self):
        return '''
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''


class PartB(PartA):

    def config(self, data):
        data.pos = [[0, 0] for _ in range(10)]

    def example_answer(self):
        return 1


Day.do_day(9, 2022, PartA, PartB)
