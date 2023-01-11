import re
import numpy as np


def read_input():
    f = open('day04/input.txt')
    data = f.read().splitlines()
    f.close()

    numbers = data[0]
    boards = []

    board = np.zeros((5, 5))
    y = 0
    for board_id in range(2, len(data)):
        line = data[board_id]
        if(line == ''):
            y = 0
            boards.append(board)
            board = np.zeros((5, 5))
            continue

        row = re.split(' +', line.strip())
        for x in range(len(row)):
            board[x, y] = int(row[x])
        y += 1

    boards.append(board)

    return numbers, boards


def mark_number(number, boards, marks):
    for i in range(len(boards)):
        indices = np.where(boards[i] == int(number), 1, 0)
        marks[i] += indices


def check_win(marks):
    for i in range(len(marks)):
        board_marks = marks[i]
        row_sums = np.sum(board_marks, axis=1)
        col_sums = np.sum(board_marks, axis=0)
        if np.any(row_sums > 4) or np.any(col_sums > 4):
            return i

    return -1


def compute_score(number, board, marks):
    score = np.sum(board, where=marks == 0)
    return score * int(number)


def part_a(numbers, boards):
    marks = []
    for _ in range(len(boards)):
        marks.append(np.zeros((5, 5)))

    for num in numbers.split(','):
        mark_number(num, boards, marks)
        idx = check_win(marks)
        if idx >= 0:
            score = compute_score(num, boards[idx], marks[idx])
            print(f'winning board idx: {idx} with score: {score}')
            break


def part_b(numbers, boards):
    marks = []
    for _ in range(len(boards)):
        marks.append(np.zeros((5, 5)))

    last_board = np.zeros((5, 5))
    last_marks = np.zeros((5, 5))
    last_num = 0
    for num in numbers.split(','):
        mark_number(num, boards, marks)
        idx = check_win(marks)
        if len(boards) == 1 and idx >= 0:
            score = compute_score(num, boards[0], marks[0])
            print(f'last winning board with score: {score}')
            break
        while idx >= 0:
            last_board = boards[idx]
            last_marks = marks[idx]
            last_num = num
            del boards[idx]
            del marks[idx]
            idx = check_win(marks)
    if len(boards) > 1:
        score = compute_score(last_num, last_board, last_marks)
        print(f'last winning board with score: {score}')


def main():
    numbers, boards = read_input()
    part_a(numbers, boards)
    part_b(numbers, boards)


if __name__ == '__main__':
    main()
