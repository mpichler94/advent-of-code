import nographs

from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.cubes = set()
        for y, line in enumerate(text.splitlines()):
            for x, char in enumerate(line):
                if char == "#":
                    data.cubes.add(nographs.Position.at(x, y, 0))

        data.moves = nographs.Position.moves(dimensions=3, diagonals=True, zero_move=False)

    def compute(self, data):
        for _ in range(6):
            inactive = []
            active = []
            for cube in data.cubes:
                count = 0
                for neighbor in cube.neighbors(data.moves):
                    if neighbor in data.cubes:
                        count += 1

                if count < 2 or count > 3:
                    inactive.append(cube)

                for pos in cube.neighbors(data.moves):
                    count = 0
                    for neighbor in pos.neighbors(data.moves):
                        if neighbor in data.cubes:
                            count += 1
                    if count == 3:
                        active.append(pos)

            for cube in inactive:
                data.cubes.remove(cube)
            data.cubes.update(active)

        return len(data.cubes)

    def example_answer(self):
        return 112


class PartB(PartA):
    def config(self, data):
        cubes = set()
        for cube in data.cubes:
            cubes.add(nographs.Position.at(cube[0], cube[1], cube[2], 0))
        data.cubes = cubes
        data.moves = nographs.Position.moves(dimensions=4, diagonals=True, zero_move=False)

    def example_answer(self):
        return 848


Day.do_day(17, 2020, PartA, PartB)
