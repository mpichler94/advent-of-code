import itertools
import re
import math


def read_input():
    file = open('day18/input.txt', encoding='utf8')
    data = file.read().splitlines()
    file.close()

    return data


def add(numbers):
    left = numbers[0]
    for i in range(1, len(numbers)):
        left = f'[{left},{numbers[i]}]'
        left = reduce(left)
    return left


def reduce(number):
    reduced = explode(number)
    if reduced != number:
        return reduce(reduced)

    reduced = split(number)
    if reduced != number:
        return reduce(reduced)

    return reduced


def explode(number):
    i = 0
    while i < len(number):
        pair = re.search(r'\[(\d+),(\d+)\]', number[i:])
        if pair is None:
            break
        depth = number[:pair.start() + i].count('[')
        depth -= number[:pair.start() + i].count(']')
        if depth >= 4:
            l_add = int(pair[1])
            r_add = int(pair[2])
            left_part = number[pair.start() + i - 1::-1]
            right_part = number[pair.end() + i:]
            left = re.search(r'\d+', left_part)
            if left:
                left_part = f'{left_part[:left.start()]}{str(l_add + int(left[0][::-1]))[::-1]}{left_part[left.end():]}'
            right = re.search(r'\d+', number[pair.end() + i:])
            if right:
                right_part = f'{right_part[:right.start()]}{r_add + int(right[0])}{right_part[right.end():]}'
            number = f'{left_part[::-1]}0{right_part}'
            break

        i += pair.end()
    return number


def split(number):
    regular_num = re.search(r'\d\d', number)
    if regular_num is None:
        return number

    left = int(regular_num[0]) // 2
    right = math.ceil(int(regular_num[0]) / 2)
    number = f'{number[:regular_num.start()]}[{left},{right}]{number[regular_num.end():]}'

    return number


def magnitude(number):
    while True:
        pair = re.search(r'\[(\d+),(\d+)\]', number)
        if pair is None:
            return int(number)
        mag = 3 * int(pair[1]) + 2 * int(pair[2])
        number = f'{number[:pair.start()]}{mag}{number[pair.end():]}'


def part_a(numbers):
    number = add(numbers)
    mag = magnitude(number)

    print(f'[a] magnitude = {mag}')


def part_b(numbers):
    magnitudes = []
    for pair in itertools.permutations(numbers, 2):
        number = add(pair)
        magnitudes.append(magnitude(number))

    print(f'[b] max magnitude = {max(magnitudes)}')


def main():
    numbers = read_input()
    part_a(numbers)
    part_b(numbers)


if __name__ == '__main__':
    main()
