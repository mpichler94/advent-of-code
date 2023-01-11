import itertools

from utils.aoc_base import Day


class Elf:
    def __init__(self, id, pos):
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        self.considered_move = None
        self.last_x = self.x
        self.last_y = self.y

    def prepare_move(self, elves):
        self.last_x = self.x
        self.last_y = self.y

        available_moves = list(self.moves)
        move = self.moves.pop(0)
        self.moves.append(move)
        for x, y in itertools.product((-1, 0, 1), repeat=2):
            if x == 0 and y == 0:
                continue
            if len(available_moves) == 0:
                break
            if (self.x+x, self.y+y) in elves:
                if y < 0 and (0, -1) in available_moves:
                    available_moves.remove((0, -1))
                if y > 0 and (0, 1) in available_moves:
                    available_moves.remove((0, 1))
                if x < 0 and (-1, 0) in available_moves:
                    available_moves.remove((-1, 0))
                if x > 0 and (1, 0) in available_moves:
                    available_moves.remove((1, 0))

        if 0 < len(available_moves) < len(self.moves):
            self.considered_move = available_moves.pop(0)
        else:
            self.considered_move = None

    def move(self, elves):
        if self.considered_move is None:
            return False

        new_x = self.x + self.considered_move[0]
        new_y = self.y + self.considered_move[1]

        if (new_x, new_y) in elves:
            elves[(new_x, new_y)].go_back(elves)
            return False

        del elves[(self.x, self.y)]
        self.x = new_x
        self.y = new_y
        elves[(new_x, new_y)] = self

        return True

    def go_back(self, elves):
        del elves[(self.x, self.y)]
        self.x = self.last_x
        self.y = self.last_y
        elves[(self.x, self.y)] = self

    def __eq__(self, other):
        return self.id == other.id and self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Elf([{self.x}, {self.y}], {self.id})'


class PartA(Day):
    def parse(self, text, data):

        data.elves = {}
        i = 0
        for y, line in enumerate(text.splitlines()):
            for x, char in enumerate(line):
                if char == '#':
                    data.elves[(x, y)] = Elf(i, (x, y))
                    i += 1

    def config(self, data):
        data.num_rounds = 10

    def compute(self, data):
        i = 0
        while True:
            any_moved = self.do_round(data)
            i += 1
            if not any_moved or i >= data.num_rounds:
                break

        return self.get_bounds(data)

    @staticmethod
    def do_round(data):
        elves = list(data.elves.values())
        [elf.prepare_move(data.elves) for elf in elves]
        any_moved = sum(elf.move(data.elves) for elf in elves)
        return bool(any_moved)

    @staticmethod
    def get_bounds(data):
        min_x = 1000000
        min_y = 1000000
        max_x = -1000000
        max_y = -1000000

        for elf in data.elves.values():
            min_x = min(min_x, elf.x)
            min_y = min(min_y, elf.y)
            max_x = max(max_x, elf.x)
            max_y = max(max_y, elf.y)

        return (max_x - min_x + 1) * (max_y - min_y + 1) - len(data.elves)

    def example_answer(self):
        return 110


class PartB(PartA):
    def compute(self, data):
        i = 0
        elves = list(data.elves.values())
        while True:
            any_moved = self.do_round(data)
            i += 1
            if not any_moved or i >= 1000000:
                break

        return i

    def example_answer(self):
        return 20


Day.do_day(23, 2022, PartA, PartB)
