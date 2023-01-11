from functools import lru_cache
from collections import Counter


def read_input():
    file = open('day14/input.txt', encoding='utf8')
    data = file.read().splitlines()
    file.close()

    template = data[0]
    rules = {}
    for i in range(2, len(data)):
        line = data[i]
        rule = line.split(' -> ')
        rules[rule[0]] = rule[1]

    return template, rules


def part_a(template, rules):
    counter = Counter(process_polymer(template, rules, 10))

    min_quantity = get_min_quantity(counter)
    max_quantity = get_max_quantity(counter)

    print(f'[a] {max_quantity} - {min_quantity} = {max_quantity - min_quantity}')


def process_polymer(template, rules, iterations):

    @lru_cache(maxsize=None)    # caches inputs and outputs to skip repeating function calls
    def replace_and_count(pair, iteration):
        if(iteration >= iterations):
            return Counter()
        pair1 = pair[0] + rules[pair]
        pair2 = rules[pair] + pair[1]
        counter = Counter(list(rules[pair]))
        counter.update(replace_and_count(pair1, iteration + 1))
        counter.update(replace_and_count(pair2, iteration + 1))

        return counter

    counter = Counter(list(template))
    for i in range(len(template) - 1):
        counter.update(replace_and_count(template[i:i + 2], 0))

    return counter


def get_min_quantity(counter):
    values = counter.values()
    return min(values)


def get_max_quantity(counter):
    values = counter.values()
    return max(values)


def part_b(template, rules):
    counter = Counter(process_polymer(template, rules, 40))
    min_quantity = get_min_quantity(counter)
    max_quantity = get_max_quantity(counter)

    print(f'[b] {max_quantity} - {min_quantity} = {max_quantity - min_quantity}')


def main():
    template, rules = read_input()
    part_a(template, rules)
    part_b(template, rules)


if __name__ == '__main__':
    main()
