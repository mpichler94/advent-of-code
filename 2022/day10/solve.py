from utils.aoc_base import Day
from collections import namedtuple

Command = namedtuple('Command', ['cmd', 'param'])


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.commands = []
        for line in lines:
            if line.startswith('addx'):
                parts = line.split()
                data.commands.append(Command(parts[0], int(parts[1])))
            else:
                data.commands.append(Command('noop', 0))


    def compute(self, data):
        cycle = 1
        x = 1
        values = []
        targets = [20 + i * 40 for i in range(6)]
        sum = 0

        for command in data.commands:
            if command.cmd == 'noop':
                cycle += 1
            else:
                cycle += 1
                if cycle in targets:
                    values.append(x)
                    sum += x * cycle
                cycle += 1
                x += command.param

            if cycle in targets:
                values.append(x)
                sum += x * cycle

        return sum

    def example_input(self):
        return '''
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop      
'''

    def example_answer(self):
        return 13140


class PartB(PartA):
    def compute(self, data):
        cycle = 0
        x = 1
        image = []
        row = []

        for command in data.commands:
            if len(row) >= 40:
                image.append(row)
                row = []
            if abs(cycle - x - 40 * len(image)) < 2:
                row.append('#')
            else:
                row.append('.')

            if command.cmd == 'noop':
                cycle += 1
            else:
                cycle += 1
                if len(row) >= 40:
                    image.append(row)
                    row = []
                if abs(cycle - x - 40 * len(image)) < 2:
                    row.append('#')
                else:
                    row.append('.')
                cycle += 1
                x += command.param

        image.append(row)
        print('[b] lit pixels:')
        for i in range(len(image)):
            line = ''.join(image[i])
            print(f'{line}')

    def example_answer(self):
        return


Day.do_day(10, 2022, PartA, PartB)
