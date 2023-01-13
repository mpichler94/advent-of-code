from utils.aoc_base import Day
import re
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.numbers = [int(num) for num in lines[0].split(',')]
        data.boards = []

        board = np.zeros((5, 5), dtype=int)
        y = 0
        for board_id in range(2, len(lines)):
            line = lines[board_id]
            if line == '':
                y = 0
                data.boards.append(board)
                board = np.zeros((5, 5), dtype=int)
                continue

            row = re.split(' +', line.strip())
            for x in range(len(row)):
                board[x, y] = int(row[x])
            y += 1

        data.boards.append(board)

    def compute(self, data):
        marks = [np.zeros((5, 5), dtype=int) for _ in range(len(data.boards))]

        for num in data.numbers:
            self.mark_number(num, data.boards, marks)
            idx = self.check_win(marks)
            if idx >= 0:
                score = self.compute_score(num, data.boards[idx], marks[idx])
                return int(score)

    @staticmethod
    def mark_number(number, boards, marks):
        for i in range(len(boards)):
            indices = np.where(boards[i] == number, 1, 0)
            marks[i] += indices

    @staticmethod
    def check_win(marks):
        for i in range(len(marks)):
            board_marks = marks[i]
            row_sums = np.sum(board_marks, axis=1)
            col_sums = np.sum(board_marks, axis=0)
            if np.any(row_sums > 4) or np.any(col_sums > 4):
                return i

        return -1

    @staticmethod
    def compute_score(number, board, marks):
        score = np.sum(board, where=marks == 0, dtype=int)
        return score * int(number)

    def example_answer(self):
        return 4512


class PartB(PartA):
    def compute(self, data):
        marks = [np.zeros((5, 5), dtype=int) for _ in range(len(data.boards))]

        last_board = np.zeros((5, 5), dtype=int)
        last_marks = np.zeros((5, 5), dtype=int)
        last_num = 0
        for num in data.numbers:
            self.mark_number(num, data.boards, marks)
            idx = self.check_win(marks)
            if len(data.boards) == 1 and idx >= 0:
                score = self.compute_score(num, data.boards[0], marks[0])
                return int(score)
            while idx >= 0:
                last_board = data.boards[idx]
                last_marks = marks[idx]
                last_num = num
                del data.boards[idx]
                del marks[idx]
                idx = self.check_win(marks)
        if len(data.boards) > 1:
            score = self.compute_score(last_num, last_board, last_marks)
            return int(score)

    def example_answer(self):
        return 1924


Day.do_day(4, 2021, PartA, PartB)
