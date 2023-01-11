import parse
import math
import itertools
import numpy as np


def read_input():
    file = open('day17/input.txt', encoding='utf8')
    data = file.read()
    file.close()

    result = parse.parse('target area: x={:d}..{:d}, y={:d}..{:d}', data)

    return result


def compute_velocity_a(target_area):
    v_x = int(round((-1 + math.sqrt(1 + 8 * target_area[0])) / 2))
    v_y = int(-target_area[2] - 1)
    return v_x, v_y


def compute_max_height(v_y):
    return int(v_y * (v_y + 1) / 2)


def get_possible_velocities(target_area):
    min_x = int(math.ceil((-1 + math.sqrt(1 + 8 * target_area[0])) / 2))
    max_x = int(target_area[1])
    min_y = int(target_area[2])
    max_y = int(-target_area[2] - 1)
    return min_x, max_x, min_y, max_y


def check_hit(velocity, target_area):
    x = 0
    y = 0
    v_x = velocity[0]
    v_y = velocity[1]
    while True:
        x += v_x
        y += v_y

        v_x -= np.sign(v_x)
        v_y -= 1

        if x > target_area[1]:
            return False
        if y < target_area[2]:
            return False
        if x >= target_area[0] and y <= target_area[3]:
            return True


def part_a(target_area):
    v_x, v_y = compute_velocity_a(target_area)
    height = compute_max_height(v_y)

    print(f'[a] highest y position = {height}')


def part_b(target_area):
    min_x, max_x, min_y, max_y = get_possible_velocities(target_area)
    velocities = list(itertools.product(range(min_x, max_x + 1), range(min_y, max_y + 1)))
    hits = 0
    for velocity in velocities:
        if check_hit(velocity, target_area):
            hits += 1
    print(f'[b] number of trajectories = {hits}')


def main():
    target_area = read_input()
    part_a(target_area)
    part_b(target_area)


if __name__ == '__main__':
    main()
