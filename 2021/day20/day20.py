from utils.aoc_base import Day
import numpy as np


class PartA(Day):
    def parse(self, text, data):
        lut, image = text.split("\n\n")

        data.lut = [1 if char == "#" else 0 for char in lut]
        data.image = [
            [1 if char == "#" else 0 for char in line] for line in image.splitlines()
        ]

        data.lut = np.array(data.lut, dtype=int)
        data.image = np.array(data.image, dtype=int)

    def config(self, data):
        data.num_rounds = 2

    def compute(self, data):
        background = 0
        for _ in range(data.num_rounds):
            data.image = self.enhance(data.lut, data.image, background)
            background = data.lut[0 if background == 0 else 1]

        return int(np.sum(data.image == 1))

    def enhance(self, lut, image, background):
        width, height = image.shape
        new_image = np.zeros((width + 2, height + 2), dtype=int)
        for y in range(-1, height + 1):
            for x in range(-1, width + 1):
                w = self.get_window(image, x, y, background)
                v = self.get_enhanced_value(lut, w)
                new_image[y + 1, x + 1] = v

        return new_image

    @staticmethod
    def get_window(image, c_x, c_y, background):
        window = np.full((3, 3), background, dtype=int)
        width, height = image.shape

        for y in range(c_y - 1, c_y + 2):
            for x in range(c_x - 1, c_x + 2):
                if y < 0 or y >= height or x < 0 or x >= width:
                    continue
                window[y - c_y + 1, x - c_x + 1] = image[y, x]

        return window

    @staticmethod
    def get_enhanced_value(lut, window):
        flattened = np.reshape(window, 9)
        index = 0
        for i in range(len(flattened)):
            index += flattened[i] << 8 - i
        return lut[index]

    def example_answer(self):
        return 35

    def example_input(self):
        return """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#. .#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#..... .#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.. ...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#..... ..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


class PartB(PartA):
    def config(self, data):
        data.num_rounds = 50

    def example_answer(self):
        return 3351


Day.do_day(20, 2021, PartA, PartB)
