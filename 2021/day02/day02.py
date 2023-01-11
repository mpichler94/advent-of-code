def read_input():
    f = open('day02/input.txt')
    lines = f.readlines()
    f.close()

    cmds = []
    nums = []

    for line in lines:
        words = line.split(' ')
        cmds.append(words[0])
        nums.append(words[1])

    return cmds, nums


def parse_input(commands, numbers):
    depth = 0
    pos = 0
    for cmd, num in zip(commands, numbers):
        if cmd == 'forward':
            pos += int(num)
        elif cmd == 'down':
            depth += int(num)
        else:
            depth -= int(num)

    return pos, depth


def parse_manual(commands, numbers):
    aim = 0
    pos = 0
    depth = 0

    for cmd, num in zip(commands, numbers):
        if cmd == 'forward':
            pos += int(num)
            depth += aim * int(num)
        elif cmd == 'down':
            aim += int(num)
        else:
            aim -= int(num)
    return pos, depth


def main():
    commands, numbers = read_input()
    pos, depth = parse_input(commands, numbers)

    print(f'x: {pos} y: {depth} product: {pos * depth}')

    pos, depth = parse_manual(commands, numbers)

    print(f'x: {pos} y: {depth} product: {pos * depth}')


if __name__ == '__main__':
    main()
