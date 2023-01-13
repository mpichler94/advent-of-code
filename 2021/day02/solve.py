from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()
        data.commands = [[x for x in line.split(' ')] for line in lines]

    def compute(self, data):
        depth = 0
        pos = 0
        for command in data.commands:
            cmd = command[0]
            num = int(command[1])
            if cmd == 'forward':
                pos += num
            elif cmd == 'down':
                depth += num
            else:
                depth -= num

        return pos * depth


class PartB(PartA):
    def compute(self, data):
        aim = 0
        pos = 0
        depth = 0

        for command in data.commands:
            cmd = command[0]
            num = int(command[1])
            if cmd == 'forward':
                pos += int(num)
                depth += aim * int(num)
            elif cmd == 'down':
                aim += int(num)
            else:
                aim -= int(num)
        return pos * depth


Day.do_day(2, 2021, PartA, PartB)
