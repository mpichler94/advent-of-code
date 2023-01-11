import numpy as np


def read_input():
    f = open('day05/input.txt')
    lines = f.read().splitlines()

    v_lines = []    # x, y1, y2
    h_lines = []    # y, x1, x2
    dd_lines = []   # l, x1, y1  i.e. 3,1 -> 5,3
    du_lines = []   # l, x1, y1  i.e. 3,5 -> 5,3

    for idx in range(len(lines)):
        line = lines[idx]
        x1, x2, y1, y2 = get_points(line)

        if x1 == x2:
            add_vline(v_lines, x1, y1, y2)

        elif y1 == y2:
            add_hline(h_lines, y1, x1, x2)

        else:
            add_dline(dd_lines, du_lines, x1, x2, y1, y2)

    return h_lines, v_lines, dd_lines, du_lines


def get_points(line):
    data = line.split('->')
    xy = data[0].split(',')
    x1 = int(xy[0].strip())
    y1 = int(xy[1].strip())
    xy = data[1].split(',')
    x2 = int(xy[0].strip())
    y2 = int(xy[1].strip())
    return x1, x2, y1, y2


def add_vline(v_lines, x, y1, y2):
    if y1 > y2:
        y1, y2 = y2, y1

    v_lines.append([x, y1, y2])


def add_hline(h_lines, y, x1, x2):
    if x1 > x2:
        x1, x2 = x2, x1

    h_lines.append([y, x1, x2])


def add_dline(dd_lines, du_lines, x1, x2, y1, y2):
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    if y1 < y2:
        dd_lines.append([x2 - x1, x1, y1])

    if y1 > y2:
        du_lines.append([x2 - x1, x1, y1])


def get_field_size(h_lines, v_lines):
    max_x = 0
    max_y = 0
    for line in h_lines:
        if line[0] > max_y:
            max_y = line[0]
        if line[2] > max_x:
            max_x = line[2]

    for line in v_lines:
        if line[0] > max_x:
            max_x = line[0]
        if line[2] > max_y:
            max_y = line[2]

    return max_x + 1, max_y + 1


def part_a(h_lines, v_lines):
    width, height = get_field_size(h_lines, v_lines)
    diagram = np.zeros((width, height))

    for line in h_lines:
        for x in range(line[1], line[2] + 1):
            diagram[x, line[0]] += 1
    for line in v_lines:
        for y in range(line[1], line[2] + 1):
            diagram[line[0], y] += 1

    num = np.count_nonzero(diagram > 1)
    print(f'num overlapping points: {num}')


def part_b(h_lines, v_lines, dd_lines, du_lines):
    width, height = get_field_size(h_lines, v_lines)
    diagram = np.zeros((width, height))

    for line in h_lines:
        for x in range(line[1], line[2] + 1):
            diagram[x, line[0]] += 1
    for line in v_lines:
        for y in range(line[1], line[2] + 1):
            diagram[line[0], y] += 1
    for line in dd_lines:
        for i in range(line[0] + 1):
            diagram[line[1] + i, line[2] + i] += 1
    for line in du_lines:
        for i in range(line[0] + 1):
            diagram[line[1] + i, line[2] - i] += 1

    num = np.count_nonzero(diagram > 1)
    print(f'num overlapping points: {num}')


def main():
    h_lines, v_lines, dd_lines, du_lines = read_input()
    part_a(h_lines, v_lines)
    part_b(h_lines, v_lines, dd_lines, du_lines)


if __name__ == '__main__':
    main()
