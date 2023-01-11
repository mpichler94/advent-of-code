
import numpy as np


def read_input():
    f = open('day09/input.txt')
    data = f.read().splitlines()
    f.close()

    heights = []

    for row in data:
        height_row = []
        for char in row:
            height_row.append(int(char))
        heights.append(height_row)

    heights = np.array(heights)

    return heights


def part_a(heights):
    risk_sum = 0
    risk_points = []
    for x in range(heights.shape[0]):
        for y in range(heights.shape[1]):
            if is_risk_point(heights, x, y):
                risk_sum += heights[x, y] + 1
                risk_points.append([x, y])

    print(f'sum of all risk levels is {risk_sum}')
    return risk_points


def is_risk_point(heights, x, y):
    neighbors = get_neighbor_heights(heights, x, y)
    for neighbor in neighbors:
        if neighbor <= heights[x, y]:
            return False

    return True


def get_neighbor_heights(heights, x, y):
    neighbors = []
    if x > 0:
        neighbors.append(heights[x - 1, y])
    if y > 0:
        neighbors.append(heights[x, y - 1])
    if x < heights.shape[0] - 1:
        neighbors.append(heights[x + 1, y])
    if y < heights.shape[1] - 1:
        neighbors.append(heights[x, y + 1])

    return neighbors


def get_neighbors(heights, x, y):
    neighbors = []
    if x > 0:
        neighbors.append([x - 1, y])
    if y > 0:
        neighbors.append([x, y - 1])
    if x < heights.shape[0] - 1:
        neighbors.append([x + 1, y])
    if y < heights.shape[1] - 1:
        neighbors.append([x, y + 1])

    return neighbors


def part_b(heights, risk_points):
    basin_sizes = []
    for risk_point in risk_points:
        basin_points = []
        pending = []
        pending.append(risk_point)
        while len(pending) > 0:
            x, y = pending.pop()
            if [x, y] in basin_points or heights[x, y] == 9:
                continue
            basin_points.append([x, y])
            neighbors = get_neighbors(heights, x, y)
            neighbors = [neighbor for neighbor in neighbors if neighbor not in pending]
            neighbors = [neighbor for neighbor in neighbors if neighbor not in basin_points]
            pending.extend(neighbors)

        basin_sizes.append(len(basin_points))

    basin_sizes.sort()
    ret = basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]

    print(f'sum of all outputs is {ret}')


def main():
    heights = read_input()
    risk_points = part_a(heights)
    part_b(heights, risk_points)


if __name__ == '__main__':
    main()
