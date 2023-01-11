import numpy as np


def read_input():
    file = open('day11/input.txt', encoding='utf8')
    data = file.read().splitlines()
    file.close()

    energy_levels = np.zeros((10, 10))
    for y in range(10):
        for x in range(10):
            energy_levels[x, y] = int(data[y][x])

    return energy_levels


def part_a(energy_levels):
    flashes = 0
    for _ in range(100):
        energy_levels, step_flashes = step(energy_levels)
        flashes += step_flashes

    print(f'{flashes} flashes after 100 steps')


def step(energy_levels):
    energy_levels += 1
    process_flashes(energy_levels)
    step_flashes = count_flashed(energy_levels)
    energy_levels = reset_fired(energy_levels)

    return energy_levels, step_flashes


def process_flashes(energy_levels):
    flashed = True
    flashed_positions = []
    while flashed:
        flashed = False
        for y in range(10):
            for x in range(10):
                if energy_levels[x, y] > 9 and [x, y] not in flashed_positions:
                    flashed = True
                    flash(energy_levels, x, y)
                    flashed_positions.append([x, y])


def flash(energy_levels, center_x, center_y):
    for y in range(max(0, center_y - 1), min(center_y + 1, 9) + 1):
        for x in range(max(0, center_x - 1), min(center_x + 1, 9) + 1):
            if x != center_x or y != center_y:
                energy_levels[x, y] += 1


def count_flashed(energy_levels):
    return np.sum(np.where(energy_levels > 9, 1, 0))


def reset_fired(energy_levels):
    energy_levels = np.where(energy_levels > 9, 0, energy_levels)
    return energy_levels


def part_b(energy_levels):
    flashes = 0
    steps = 1
    while flashes != 100:
        energy_levels, flashes = step(energy_levels)
        steps += 1

    print(f'simultaneous flash after {steps} steps')


def main():
    energy_levels = read_input()
    part_a(energy_levels)
    part_b(energy_levels)


if __name__ == '__main__':
    main()
