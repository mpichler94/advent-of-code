import numpy as np

from utils.aoc_base import Day


class PartA(Day):
    # Board: 0..void 1..empty 2..wall
    def parse(self, text, data):
        board = []
        lines = text.splitlines()
        end = False
        for line in lines:
            row = []
            if line == '':
                end = True
                continue
            if end:
                data.path = self.parse_path(line)
                break
            for char in line:
                if char == ' ':
                    row.append(0)
                elif char == '.':
                    row.append(1)
                elif char == '#':
                    row.append(2)
            board.append(row)

        max_len = max(len(x) for x in board) + 2
        for row in board:
            row.insert(0, 0)
            for _ in range(max_len - len(row)):
                row.append(0)
        board.insert(0, [0 for _ in range(max_len)])
        board.append([0 for _ in range(max_len)])

        data.board = np.array(board)
        data.board = np.transpose(data.board)

    @staticmethod
    def parse_path(line):
        instructions = []
        command = ''
        for char in line:
            if char.isnumeric():
                command += char
                continue

            if command != '':
                instructions.append(int(command))
                command = ''

            instructions.append(char)

        instructions.append(int(command))

        return instructions

    def compute(self, data):
        pos = self.find_start(data)
        direction = 0
        for instruction in data.path:
            if type(instruction) == str:
                if instruction == 'R':
                    direction = (direction + 1) % 4
                else:
                    direction = (direction - 1) % 4
                continue

            for _ in range(instruction):
                new_pos = self.step(data.board, pos, direction)
                if new_pos == pos:
                    break
                pos = new_pos

        return 1000 * pos[1] + 4 * pos[0] + direction

    @staticmethod
    def find_start(data):
        for y in range(data.board.shape[1]):
            for x in range(data.board.shape[0]):
                if data.board[x, y] == 1:
                    return x, y

        raise RuntimeError('Cannot find start position')

    @staticmethod
    def step(board, pos, direction):
        new_x = pos[0]
        new_y = pos[1]

        if direction == 0:
            new_x = pos[0] + 1
        elif direction == 2:
            new_x = pos[0] - 1
        elif direction == 1:
            new_y = pos[1] + 1
        elif direction == 3:
            new_y = pos[1] - 1
        else:
            raise RuntimeError('Invalid direction')

        if board[new_x, new_y] == 2:
            return pos

        if board[new_x, new_y] == 0:
            if direction == 0:
                for new_x in range(new_x-1, -1, -1):
                    if board[new_x, new_y] == 0 and board[new_x+1, new_y] == 1:
                        return new_x+1, new_y
            if direction == 2:
                for new_x in range(new_x+1, board.shape[0]):
                    if board[new_x, new_y] == 0 and board[new_x-1, new_y] == 1:
                        return new_x-1, new_y
            if direction == 1:
                for new_y in range(new_y-1, -1, -1):
                    if board[new_x, new_y] == 0 and board[new_x, new_y+1] == 1:
                        return new_x, new_y+1
            if direction == 3:
                for new_y in range(new_y+1, board.shape[1]):
                    if board[new_x, new_y] == 0 and board[new_x, new_y-1] == 1:
                        return new_x, new_y-1
            return pos

        return new_x, new_y

    def example_answer(self):
        return 6032


class PartB(PartA):
    def config(self, data):
        if data.board.shape[0] == 18:   # Example
            data.side_len = 4
            data.sides = [(9, 1), (1, 5), (5, 5), (9, 5), (9, 9), (13, 9)]  # Start positions of cube sides
            # 0r 1d 2l 3u
            # dict with (side, direction) as key -> adjacent (side, direction) as value
            data.transitions = {(0, 0): (5, 2),
                                (0, 2): (2, 1),
                                (0, 3): (1, 1),
                                (1, 1): (4, 3),
                                (1, 2): (6, 3),
                                (1, 3): (0, 1),
                                (2, 1): (4, 0),
                                (2, 3): (0, 0),
                                (3, 0): (5, 1),
                                (4, 1): (1, 3),
                                (4, 2): (2, 3),
                                (5, 0): (0, 2),
                                (5, 1): (1, 0),
                                (5, 3): (3, 2),
                                }
        else:
            data.side_len = 50
            data.sides = [(51, 1), (101, 1), (51, 51), (1, 101), (51, 101), (1, 151)]  # Start positions of cube sides
            data.transitions = {(0, 2): (3, 0),
                                (0, 3): (5, 0),
                                (1, 0): (4, 2),
                                (1, 1): (2, 2),
                                (1, 3): (5, 3),
                                (2, 0): (1, 3),
                                (2, 2): (3, 1),
                                (3, 2): (0, 0),
                                (3, 3): (2, 0),
                                (4, 0): (1, 2),
                                (4, 1): (5, 2),
                                (5, 0): (4, 3),
                                (5, 1): (1, 1),
                                (5, 2): (0, 1),
                                }

    def compute(self, data):
        pos = self.find_start(data)
        direction = 0
        side = 0
        i = 0
        for instruction in data.path:
            if type(instruction) == str:
                if instruction == 'R':
                    direction = (direction + 1) % 4
                else:
                    direction = (direction - 1) % 4
                i += 1
                continue

            for _ in range(instruction):
                new_pos, direction, side = self.step(data, side, pos, direction)
                if new_pos == pos:
                    break
                pos = new_pos
                i += 1

        return 1000 * pos[1] + 4 * pos[0] + direction


    def step(self, data, side, pos, direction):
        new_x = pos[0]
        new_y = pos[1]
        new_side = side
        new_direction = direction

        if direction == 0:
            new_x = pos[0] + 1
        elif direction == 2:
            new_x = pos[0] - 1
        elif direction == 1:
            new_y = pos[1] + 1
        elif direction == 3:
            new_y = pos[1] - 1
        else:
            raise RuntimeError('Invalid direction')

        if data.board[new_x, new_y] == 2:
            return pos, direction, side

        origin = data.sides[side]

        if data.board[new_x, new_y] == 0:
            if (side, direction) not in data.transitions:
                raise RuntimeError('Impossible')
                return pos, direction, side
            new_side, new_direction = data.transitions[(side, direction)]
            new_origin = data.sides[new_side]

            if direction == 0:
                match new_direction:
                    case 0:
                        new_x = new_origin[0]
                        new_y = new_origin[1] + pos[1] - origin[1]
                    case 1:
                        new_x = new_origin[0] + origin[1] + data.side_len - 1 - pos[1]
                        new_y = new_origin[1]
                    case 2:
                        new_x = new_origin[0] + data.side_len - 1
                        new_y = new_origin[1] + origin[1] + data.side_len - 1 - pos[1]
                    case 3:
                        new_x = new_origin[0] + pos[1] - origin[1]
                        new_y = new_origin[1] + data.side_len - 1
            elif direction == 1:
                match new_direction:
                    case 0:
                        new_x = new_origin[0]
                        new_y = new_origin[1] + origin[0] + data.side_len - 1 - pos[0]
                    case 1:
                        new_x = new_origin[0] + pos[0] - origin[0]
                        new_y = new_origin[1]
                    case 2:
                        new_x = new_origin[0] + data.side_len - 1
                        new_y = new_origin[1] + pos[0] - origin[0]
                    case 3:
                        new_x = new_origin[0] + origin[0] + data.side_len - 1 - pos[0]
                        new_y = new_origin[1] + data.side_len - 1
            elif direction == 2:
                match new_direction:
                    case 0:
                        new_x = new_origin[0]
                        new_y = new_origin[1] + origin[1] + data.side_len - 1 - pos[1]
                    case 1:
                        new_x = new_origin[0] + pos[1] - origin[1]
                        new_y = new_origin[1]
                    case 2:
                        new_x = new_origin[0] + data.side_len - 1
                        new_y = new_origin[1] + pos[1] - origin[1]
                    case 3:
                        new_x = new_origin[0] + origin[1] + data.side_len - 1 - pos[1]
                        new_y = new_origin[1] + data.side_len - 1
            elif direction == 3:
                match new_direction:
                    case 0:
                        new_x = new_origin[0]
                        new_y = new_origin[1] + pos[0] - origin[0]
                    case 1:
                        new_x = new_origin[0] + origin[0] + data.side_len - 1 - pos[0]
                        new_y = new_origin[1]
                    case 2:
                        new_x = new_origin[0] + data.side_len - 1
                        new_y = new_origin[1] + origin[0] + data.side_len-1 - pos[0]
                    case 3:
                        new_x = new_origin[0] + pos[0] - origin[0]
                        new_y = new_origin[1] + data.side_len - 1

            if data.board[new_x, new_y] == 2:
                return pos, direction, side

        new_side = self.get_side(data, new_side, new_x, new_y)

        return (new_x, new_y), new_direction, new_side

    @staticmethod
    def get_side(data, old_side, x, y):
        for side, origin in enumerate(data.sides):
            if origin[0] <= x < origin[0] + data.side_len and origin[1] <= y < origin[1] + data.side_len:
                return side

        return old_side

    def example_answer(self):
        return 5031


Day.do_day(22, 2022, PartA, PartB)
