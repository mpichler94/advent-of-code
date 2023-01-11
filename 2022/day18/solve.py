import itertools

from utils.aoc_base import Day


class PartA(Day):

    def parse(self, text: str, data):
        lines = text.splitlines()
        cubes = [[int(v) for v in line.strip().split(',')] for line in lines]
        data.cubes = cubes

    @staticmethod
    def is_touching(cube, cube2):
        norm = abs(cube[0] - cube2[0]) + abs(cube[1] - cube2[1]) + abs(cube[2] - cube2[2])
        return norm == 1

    def compute(self, data):
        touching = 0
        for cube, cube2 in itertools.combinations(data.cubes, 2):
            if cube == cube2:
                continue

            if self.is_touching(cube, cube2):
                touching += 1

        return len(data.cubes) * 6 - touching * 2

    def example_answer(self):
        return 64


class PartB(PartA):
    def config(self, data):
        min_bound = [1000, 1000, 1000]
        max_bound = [-1000, -1000, -1000]

        for cube in data.cubes:
            for i in range(3):
                min_bound[i] = min(min_bound[i], cube[i]-1)
                max_bound[i] = max(max_bound[i], cube[i]+1)

        data.min_bound = min_bound
        data.max_bound = max_bound

    def compute(self, data):
        touching = 0
        seen = []

        exterior = []
        todo = [data.min_bound]
        while len(todo) > 0:
            cube = todo.pop(0)

            if cube in exterior:
                continue

            if cube in data.cubes:
                continue

            if cube[0] < data.min_bound[0] or cube[1] < data.min_bound[1] or cube[2] < data.min_bound[2]:
                continue
            if cube[0] > data.max_bound[0] or cube[1] > data.max_bound[1] or cube[2] > data.max_bound[2]:
                continue

            exterior.append(cube)

            todo.append([cube[0]+1, cube[1], cube[2]])
            todo.append([cube[0], cube[1]+1, cube[2]])
            todo.append([cube[0], cube[1], cube[2]+1])
            todo.append([cube[0]-1, cube[1], cube[2]])
            todo.append([cube[0], cube[1]-1, cube[2]])
            todo.append([cube[0], cube[1], cube[2]-1])

        for i in range(len(data.cubes)):
            touching += sum(1 for cube2 in exterior if self.is_touching(data.cubes[i], cube2))
            seen.append(data.cubes[i])

        return touching

    def example_answer(self):
        return 58


Day.do_day(18, 2022, PartA, PartB)