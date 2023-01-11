import numpy as np


def read_input():
    file = open('day13/input.txt', encoding='utf8')
    data = file.read().splitlines()
    file.close()

    positions = []
    folds = []
    for line in data:
        if line.startswith('fold'):
            fold = line.split('=')
            folds.append([fold[0][-1:], int(fold[1])])
        elif line != '':
            pos = line.split(',')
            positions.append([int(pos[0]), int(pos[1])])

    positions.sort()

    return positions, folds


def part_a(points, folds):
    fold = folds[0]
    if fold[0] == 'x':
        fold_horizontal(points, fold[1])
    else:
        fold_vertical(points, fold[1])

    points = discard_overlaps(points)

    print(f'[a] {len(points)} points')


def part_b(points, folds):
    for fold in folds:
        if fold[0] == 'x':
            fold_horizontal(points, fold[1])
        else:
            fold_vertical(points, fold[1])

        points = discard_overlaps(points)

    print(f'[a] {len(points)} points')
    print_points(points)


def fold_horizontal(points, folding_pos):
    for i in range(len(points)):
        pos = points[i]
        if pos[0] < folding_pos:
            continue
        points[i][0] = 2 * folding_pos - pos[0]


def fold_vertical(points, folding_pos):
    for i in range(len(points)):
        pos = points[i]
        if pos[1] < folding_pos:
            continue
        points[i][1] = 2 * folding_pos - pos[1]


def discard_overlaps(points):
    unique_points = []
    for point in points:
        if point in unique_points:
            continue
        unique_points.append(point)
    return unique_points


def print_points(points):
    width, height = get_dimension(points)
    grid = np.zeros((height, width))
    for point in points:
        grid[point[1], point[0]] = 1

    output = ''
    for line in grid:
        output += '\n' + ''.join([' ' if val == 0 else '#' for val in line])

    print(output)


def get_dimension(points):
    max_x = 0
    max_y = 0
    for p in points:
        if p[0] > max_x:
            max_x = p[0]
        if p[1] > max_y:
            max_y = p[1]

    return max_x + 1, max_y + 1


def main():
    points, folds = read_input()
    part_a(points, folds)
    part_b(points, folds)


if __name__ == '__main__':
    main()
