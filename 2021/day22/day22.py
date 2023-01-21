from utils.aoc_base import Day
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


class PartA(Day):
    def parse(self, text, data):
        data.steps = []
        for line in text.splitlines():
            on = line.startswith('on')
            result = parse.parse('{:w} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}', line)
            data.steps.append(Step(on, (result[1], result[2]), (result[3], result[4]), (result[5], result[6])))

    def compute(self, data):
        unique_steps = []

        for step in data.steps:
            if step.x[0] < -50 or step.x[1] > 50 or step.y[0] < -50 or step.y[1] > 50 or step.z[0] < -50 or step.z[1] > 50:
                continue
            unique_steps.extend(self.get_intersections(unique_steps, step))
            if step.on:
                unique_steps.append(step)
        return sum(step.cubes() for step in unique_steps)

    def get_intersections(self, steps, step):
        intersections = []
        for prev_step in steps:
            intersection = self.get_intersection(not prev_step.on, prev_step, step)
            if intersection is not None:
                intersections.append(intersection)
        return intersections

    @staticmethod
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


class PartB(PartA):
    def compute(self, data):
        unique_steps = []

        for step in data.steps:
            unique_steps.extend(self.get_intersections(unique_steps, step))
            if step.on:
                unique_steps.append(step)

        return sum(step.cubes() for step in unique_steps)


Day.do_day(22, 2021, PartA, PartB)
