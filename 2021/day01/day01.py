import numpy as np


def read_input():
    data = np.loadtxt('day01/input.txt')
    return data


def count_increases(data):
    diff = np.diff(data)
    count = np.count_nonzero(diff > 0)
    return count


def create_mean(data):
    ret = np.convolve(data, np.ones(3))
    return ret[2:]


def main():
    data = read_input()
    count = count_increases(data)

    print(f'{count} times increasing')

    data = create_mean(data)
    count = count_increases(data)

    print(f'{count} times increasing with mean')


if __name__ == '__main__':
    main()
