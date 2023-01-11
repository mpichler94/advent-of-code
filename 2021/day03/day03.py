def read_input():
    f = open('day03/input.txt')
    data = f.read().splitlines()
    f.close()
    return data


def get_most_common(data):
    num_bits = len(data[0])
    one_bits = [0] * num_bits
    for number in data:
        for i in range(len(number)):
            if number[i] == '1':
                one_bits[i] += 1

    num = len(data)
    most_common = ''
    for i in range(len(one_bits)):
        zero_bits = num - one_bits[i]
        if one_bits[i] > zero_bits:
            most_common += '1'
        elif one_bits[i] < zero_bits:
            most_common += '0'
        else:
            most_common += '1'

    return most_common


def get_most_common_numbers(data, i):
    ret = []
    most_common = get_most_common(data)
    for number in data:
        if number[i] == most_common[i]:
            ret.append(number)

    return ret


def get_least_common_numbers(data, i):
    ret = []
    most_common = get_most_common(data)
    for number in data:
        if number[i] != most_common[i]:
            ret.append(number)

    return ret


def get_oxygen(data):
    data = data.copy()
    for i in range(len(data[0])):
        data = get_most_common_numbers(data, i)

    return data[0]


def get_co2(data):
    data = data.copy()
    for i in range(len(data[0])):
        data = get_least_common_numbers(data, i)
        if len(data) == 1:
            break
    return data[0]


def bin_to_dec(number):
    ret = 0
    for i in range(len(number)):
        if(number[i] == '1'):
            ret += 1 << (len(number) - i - 1)

    return ret


def invert_bits(number):
    ret = ''
    for i in range(len(number)):
        if(number[i] == '1'):
            ret += '0'
        else:
            ret += '1'

    return ret


def main():
    data = read_input()
    most_common = get_most_common(data)
    gamma = bin_to_dec(most_common)
    epsilon = bin_to_dec(invert_bits(most_common))

    print(f'gamma: {gamma} sigma: {epsilon} consumption {gamma * epsilon}')

    oxygen = get_oxygen(data)
    oxygen = bin_to_dec(oxygen)

    co2 = get_co2(data)
    co2 = bin_to_dec(co2)

    print(f'oxygen: {oxygen} CO2: {co2} life support: {oxygen * co2}')


if __name__ == '__main__':
    main()
