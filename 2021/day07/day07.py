import numpy as np


def read_input():
    crabs = np.loadtxt('day07/input.txt', dtype=int, delimiter=',')
    return crabs


def cost_a(pos, crabs):
    return np.sum(np.abs(pos - crabs))


def cost_b(pos, crabs):
    diff = np.abs(pos - crabs)
    return np.sum(diff * (diff + 1) / 2)


def all_costs(crabs, cost_function):
    max_pos = np.max(crabs)
    costs = np.zeros(max_pos + 1)
    for i in range(max_pos + 1):
        costs[i] = cost_function(i, crabs)

    return costs


def part_a(crabs):
    costs = all_costs(crabs, cost_a)
    idx = np.argmin(costs)
    print(f'moving all crabs to {idx} spends {int(costs[idx])} fuel')


def part_b(crabs):
    costs = all_costs(crabs, cost_b)
    idx = np.argmin(costs)
    print(f'moving all crabs to {int(idx)} spends {int(costs[idx])} fuel')


def main():
    crabs = read_input()
    part_a(crabs)
    part_b(crabs)


if __name__ == '__main__':
    main()
