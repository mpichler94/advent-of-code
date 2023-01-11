from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()
        data.trees = [[int(char) for char in line] for line in lines]

    def compute(self, data):
        width = len(data.trees)
        height = len(data.trees[0])

        visible = 0
        for y in range(height):
            for x in range(width):
                visible += self.is_visible(data.trees, x, y)

        return visible

    @staticmethod
    def is_visible(trees, x, y):
        width = len(trees)
        height = len(trees[0])
        if x == 0 or x == width or y == 0 or y == height:
            return True
        tree = trees[y][x]
        larger = 4
        for i in range(x+1, width):
            if trees[y][i] >= tree:
                larger -= 1
                break
        for i in range(x):
            if trees[y][i] >= tree:
                larger -= 1
                break
        for i in range(y+1, height):
            if trees[i][x] >= tree:
                larger -= 1
                break
        for i in range(y):
            if trees[i][x] >= tree:
                larger -= 1
                break
        if larger > 0:
            return True

        return False

    def example_answer(self):
        return 21


class PartB(PartA):
    def compute(self, data):
        width = len(data.trees)
        height = len(data.trees[0])

        scenic_score = 0
        for y in range(height):
            if y == 0 or y == height:
                continue

            for x in range(width):
                if x == 0 or x == width:
                    continue

                distance = self.get_distances(data.trees, x, y)
                score = distance[0] * distance[1] * distance[2] * distance[3]
                scenic_score = max(scenic_score, score)

        return scenic_score

    @staticmethod
    def get_distances(trees, x, y):
        width = len(trees)
        height = len(trees[0])

        distance = [width-x-1, x, height-y-1, y]
        tree = trees[y][x]
        for i in range(x+1, width):
            if trees[y][i] >= tree:
                distance[0] = i-x
                break
        for i in range(x-1, -1, -1):
            if trees[y][i] >= tree:
                distance[1] = x - i
                break
        for i in range(y+1, height):
            if trees[i][x] >= tree:
                distance[2] = i-y
                break
        for i in range(y-1, -1, -1):
            if trees[i][x] >= tree:
                distance[3] = y - i
                break

        return distance

    def example_answer(self):
        return 8


Day.do_day(8, 2022, PartA, PartB)
