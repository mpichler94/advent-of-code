import itertools

from utils.aoc_base import Day


class PartA(Day):

    def parse(self, text, data):
        data.text = text.strip().strip('\n')
        data.jets = [-1 if c == '<' else 1 for c in data.text]
        data.jet_iterator = itertools.cycle(enumerate(data.jets))

    def config(self, data):
        rocks = []

        # -
        rock = [[1], [1], [1], [1]]
        rocks.append(rock)

        # +
        rock = [[0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]]
        rocks.append(rock)

        # J
        rock = [[0, 0, 1],
                [0, 0, 1],
                [1, 1, 1]]
        rocks.append(rock)

        # I
        rock = [[1, 1, 1, 1]]
        rocks.append(rock)

        # #
        rock = [[1, 1],
                [1, 1]]
        rocks.append(rock)

        data.rocks = rocks
        data.rock_iterator = itertools.cycle(data.rocks)

        data.cave = [[1, 1, 1, 1, 1, 1, 1]]

    def compute(self, data):
        count = 0
        while True:
            if count >= 2022:
                return len(data.cave) - 1

            self.do_rock(data)
            count += 1

    def do_rock(self, data):
        rock = next(data.rock_iterator)
        rock_pos = [2, len(data.cave) + 2 + len(rock[0])]

        while True:
            idx, jet = next(data.jet_iterator)
            self.move_h(jet, rock, rock_pos, data.cave)

            if not self.check_collision(rock, [rock_pos[0], rock_pos[1]-1], data.cave):
                rock_pos[1] -= 1
                continue

            self.update_cave(rock, rock_pos, data.cave)
            return idx

    def move_h(self, cmd, rock, rock_pos, cave):
        new_x = max(0, min(rock_pos[0] + cmd, 7 - len(rock)))
        if not self.check_collision(rock, [new_x, rock_pos[1]], cave):
            rock_pos[0] = new_x

    @staticmethod
    def check_collision(rock, rock_pos, cave):
        for x in range(len(rock)):
            for y in range(len(rock[0])):
                if rock[x][y] == 0:
                    continue

                y_pos = rock_pos[1] - y
                if y_pos < len(cave) and cave[y_pos][rock_pos[0] + x] == 1:
                    return True

        return False

    @staticmethod
    def update_cave(rock, rock_pos, cave):
        for y in range(len(rock[0])-1, -1, -1):
            for x in range(len(rock)):
                if rock[x][y] == 0:
                    continue

                y_pos = rock_pos[1] - y
                if y_pos >= len(cave):
                    cave.append([0, 0, 0, 0, 0, 0, 0])

                cave[y_pos][rock_pos[0] + x] = 1

    @staticmethod
    def check_touchdown(rock, rock_pos, heights):
        for x in range(len(rock)):
            for y in range(len(rock[0])):
                if rock[x][y] == 0:
                    continue

                if heights[rock_pos[0] + x] >= rock_pos[1] - y:
                    return True

        return False

    def example_answer(self):
        return 3068

    def example_input(self):
        return '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'


class PartB(PartA):
    def compute(self, data):
        total_rounds = 1000000000000

        count, cycle_length, cycle_height = self.find_cycle(data)

        cycle_factor = (total_rounds - count) // cycle_length
        cycle_rounds = cycle_factor * cycle_length
        rounds_todo = total_rounds - count - cycle_rounds

        for _ in range(rounds_todo):
            self.do_rock(data)

        return len(data.cave) + cycle_factor * cycle_height - 1

    def find_cycle(self, data):
        total_rounds = 1000000000000
        cycle_height = 0
        jet_indices = set()
        cycles_completed = 0
        for count in range(1, total_rounds+1):
            jet_idx = self.do_rock(data)
            if count % len(data.rocks) == 0:
                if jet_idx in jet_indices:
                    if cycles_completed == 0:
                        cycle_length = count
                        cycle_height = len(data.cave)
                        jet_indices = {jet_idx}
                        cycles_completed += 1
                    elif cycles_completed == 1:
                        cycle_height = len(data.cave) - cycle_height
                        cycle_length = count - cycle_length
                        break
                elif cycles_completed == 0:
                    jet_indices.add(jet_idx)

            count += 1

        return count, cycle_length, cycle_height

    def example_answer(self):
        return 1514285714288


Day.do_day(17, 2022, PartA, PartB)
