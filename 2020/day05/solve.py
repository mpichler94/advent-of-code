from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.commands = text.splitlines()

    def compute(self, data):
        max_id = 0
        for command in data.commands:
            max_id = max(max_id, self.get_seat_id(command))

        return max_id

    def get_seat_id(self, command):
        row, column = self.get_seat(command)
        return row * 8 + column

    def get_seat(self, command):
        rows = command[:-3]
        columns = command[-3:]
        row = self.partition(rows, 128)
        col = self.partition(columns, 8)
        return row, col

    @staticmethod
    def partition(commands, range):
        low = 0
        high = range - 1
        for c in commands:
            diff = (high - low + 1) // 2
            if c == "F" or c == "L":
                high -= diff
            else:
                low += diff
        return low

    def example_answer(self):
        return 357

    def example_input(self):
        return "FBFBBFFRLR"


class PartB(PartA):
    def compute(self, data):
        ids = [self.get_seat_id(command) for command in data.commands]
        ids.sort()
        diff = [x - y for y, x in zip(ids[:-1], ids[1:])]
        i = diff.index(2)
        return ids[i] + 1

    @staticmethod
    def calc_id(row, column):
        return row * 8 + column

    def example_answer(self):
        return 566

    def example_input(self):
        return "BFFFBBFRRR\nFFFBBBFRRR\nBBFFBBFRLL\nBFFFBBFRLR"


Day.do_day(5, 2020, PartA, PartB)
