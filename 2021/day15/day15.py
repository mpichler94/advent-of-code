import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


def read_input():
    file = open('day15/input.txt', encoding='utf8')
    data = file.read().splitlines()
    file.close()

    matrix = []
    for line in data:
        row = []
        for weight in line:
            row.append(int(weight))
        matrix.append(row)

    matrix = np.array(matrix)

    return matrix


def create_grid_a(matrix):
    grid = Grid(matrix=matrix)

    return grid


def create_grid_b(matrix):
    tile = matrix
    shape = matrix.shape
    matrix = np.zeros((shape[0] * 5, shape[1] * 5))

    for y in range(5):
        for x in range(5):
            matrix[x * shape[0]:(x + 1) * shape[0], y * shape[1]: (y + 1) * shape[1]] = tile + x + y
            matrix = np.where(matrix > 9, matrix - 9, matrix)
    grid = Grid(matrix=matrix)
    return grid


def find_path(grid):
    start = grid.node(0, 0)
    end = grid.node(-1, -1)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

    path, _ = finder.find_path(start, end, grid)

    return path


def compute_total_weight(grid, path):
    start = grid.node(0, 0)

    total_weight = sum([grid.node(pos[0], pos[1]).weight for pos in path])
    total_weight -= start.weight

    return total_weight


def part_a(matrix):
    grid = create_grid_a(matrix)
    path = find_path(grid)
    total_weight = compute_total_weight(grid, path)

    print(f'[a] total weight = {total_weight}')


def part_b(matrix):
    grid = create_grid_b(matrix)
    path = find_path(grid)
    total_weight = compute_total_weight(grid, path)

    print(f'[b] total weight = {total_weight}')


def main():
    matrix = read_input()
    part_a(matrix)
    part_b(matrix)


if __name__ == '__main__':
    main()
