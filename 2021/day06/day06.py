import numpy as np


def read_input():
    f = open('day06/input.txt')
    line = f.read()

    fish = np.zeros(9, dtype=np.longlong)
    for a_fish in line.split(','):
        days = int(a_fish)
        fish[days] += 1

    return fish


def simulate_day(fish):
    new_fish = fish[0]
    fish[0] = 0
    for i in range(1, len(fish)):
        fish[i - 1] += fish[i]
        fish[i] = 0

    fish[8] += new_fish
    fish[6] += new_fish


def simulate(fish):
    for _ in range(80):
        simulate_day(fish)
    print(f'{np.sum(fish)} lanternfish after 80 days')
    for _ in range(256 - 80):
        simulate_day(fish)
    print(f'{np.sum(fish)} lanternfish after 256 days')


def main():
    fish = read_input()
    simulate(fish)


if __name__ == '__main__':
    main()
