def read_input():
    f = open('day08/input.txt')
    data = f.read().splitlines()
    f.close()

    signal_patterns = []
    outputs = []

    for row in data:
        parts = row.split(' | ')
        patterns = []
        row_outputs = []
        for pattern in parts[0].split(' '):
            patterns.append(''.join(sorted(pattern)))
        for output in parts[1].split(' '):
            row_outputs.append(''.join(sorted(output)))

        signal_patterns.append(patterns)
        outputs.append(row_outputs)

    return signal_patterns, outputs


def part_a(outputs):
    count = 0
    for row in outputs:
        for output in row:
            length = len(output)
            if length < 5 or length == 7:
                count += 1

    print(f'{count} digits with unique number of segments')


def part_b(signal_patterns, output_values):
    output_sum = 0
    for patterns, outputs in zip(signal_patterns, output_values):
        digits = [''] * 10
        digits[1], digits[4], digits[7], digits[8] = find_unique(patterns)
        digits[6] = find_6(patterns, digits[1])
        digits[9] = find_9(patterns, digits[4])
        digits[0] = find_0(patterns, digits[6], digits[9])
        digits[3] = find_3(patterns, digits[1], digits[9])
        digits[5] = find_5(patterns, digits[6])
        digits[2] = find_2(patterns, digits[3], digits[5])

        lookup = {v: str(k) for k, v in enumerate(digits)}
        number = ''
        for output in outputs:
            number += lookup[output]
        output_sum += int(number)

    print(f'sum of all outputs is {output_sum}')


def find_unique(patterns):
    one = ''
    four = ''
    seven = ''
    eight = ''

    for pattern in patterns:
        if len(pattern) == 2:
            one = pattern
        elif len(pattern) == 3:
            seven = pattern
        elif len(pattern) == 4:
            four = pattern
        elif len(pattern) == 7:
            eight = pattern

    patterns.remove(one)
    patterns.remove(four)
    patterns.remove(seven)
    patterns.remove(eight)
    return one, four, seven, eight


def find_6(patterns, one):
    for pattern in patterns:
        if len(pattern) != 6:
            continue
        if has_one(one, pattern):
            patterns.remove(pattern)
            return pattern


def find_9(patterns, four):
    for pattern in patterns:
        if len(pattern) != 6:
            continue
        if has_all(four, pattern):
            patterns.remove(pattern)
            return pattern


def find_0(patterns, six, nine):
    for pattern in patterns:
        if len(pattern) != 6:
            continue
        if pattern is not six and pattern is not nine:
            patterns.remove(pattern)
            return pattern


def find_3(patterns, one, nine):
    for pattern in patterns:
        if len(pattern) != 5:
            continue
        if has_all(one, pattern) and has_all_but_one(nine, pattern):
            patterns.remove(pattern)
            return pattern


def find_5(patterns, six):
    for pattern in patterns:
        if len(pattern) != 5:
            continue
        if has_all(pattern, six):
            patterns.remove(pattern)
            return pattern


def find_2(patterns, three, five):
    for pattern in patterns:
        if len(pattern) != 5:
            continue
        if pattern is not three and pattern is not five:
            patterns.remove(pattern)
            return pattern


# check if all chars are in string
def has_all(chars, string):
    return all([char in string for char in chars])


# check if one and only on char is in string
def has_one(chars, string):
    checks = [char in string for char in chars]
    i = iter(checks)
    return any(i) and not any(i)


# check if all but one char is in string
def has_all_but_one(chars, string):
    checks = [char in string for char in chars]
    checks = [not check for check in checks]
    i = iter(checks)
    return any(i) and not any(i)


def main():
    patterns, outputs = read_input()
    part_a(outputs)
    part_b(patterns, outputs)


if __name__ == '__main__':
    main()
