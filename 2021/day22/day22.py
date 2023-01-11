import parse


class Step:
    def __init__(self, on: bool, x: tuple[int, int], y: tuple[int, int], z: tuple[int, int]) -> None:
        self.on = on
        self.x = x
        self.y = y
        self.z = z

    def cubes(self):
        count = (self.z[1] - self.z[0] + 1) * (self.y[1] - self.y[0] + 1) * (self.x[1] - self.x[0] + 1)
        if not self.on:
            count *= -1
        return count


def read_input():
    file = open('day22/input.txt', encoding='utf8')
    data = file.read().splitlines()
    file.close()

    steps = []
    for line in data:
        on = line.startswith('on')
        result = parse.parse('{:w} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}', line)
        steps.append(Step(on, (result[1], result[2]), (result[3], result[4]), (result[5], result[6])))

    return steps


def get_intersection(on, step1, step2):
    x = (max(step1.x[0], step2.x[0]), min(step1.x[1], step2.x[1]))
    y = (max(step1.y[0], step2.y[0]), min(step1.y[1], step2.y[1]))
    z = (max(step1.z[0], step2.z[0]), min(step1.z[1], step2.z[1]))

    if x[0] > x[1]:
        return None
    if y[0] > y[1]:
        return None
    if z[0] > z[1]:
        return None

    return Step(on, x, y, z)


def get_intersections(steps, step):
    intersections = []
    for prev_step in steps:
        intersection = None
        intersection = get_intersection(not prev_step.on, prev_step, step)
        if intersection is not None:
            intersections.append(intersection)

    return intersections


def part_a(steps):
    unique_steps = []

    for step in steps:
        if step.x[0] < -50 or step.x[1] > 50 or step.y[0] < -50 or step.y[1] > 50 or step.z[0] < -50 or step.z[1] > 50:
            continue
        unique_steps.extend(get_intersections(unique_steps, step))
        if step.on:
            unique_steps.append(step)

    count = 0
    for step in unique_steps:
        count += step.cubes()

    print(f'[a] number of cubes = {count}')


def part_b(steps):
    unique_steps = []

    for step in steps:
        unique_steps.extend(get_intersections(unique_steps, step))
        if step.on:
            unique_steps.append(step)

    count = 0
    for step in unique_steps:
        count += step.cubes()

    print(f'[b] number of cubes = {count}')


def main():
    steps = read_input()
    part_a(steps)
    part_b(steps)


if __name__ == '__main__':
    main()
