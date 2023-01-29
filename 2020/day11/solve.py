import itertools

import nographs

from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.seats = nographs.Array([[c for c in line] for line in text.splitlines()])
        data.moves = nographs.Position.moves(diagonals=True)
        data.limits = data.seats.limits()
        data.occupied_limit = 4

    def compute(self, data):
        while True:
            new_seats = self.step(data)
            if data.seats.content == new_seats.content:
                break
            data.seats = new_seats

        occupied = 0
        for x, y in itertools.product(range(data.limits[0][1]), range(data.limits[1][1])):
            if data.seats[(x, y)] == "#":
                occupied += 1
        return occupied

    @staticmethod
    def step(data):
        new_seats = data.seats.mutable_copy()
        for x, y in itertools.product(range(data.limits[0][1]), range(data.limits[1][1])):
            pos = nographs.Position.at(x, y)
            neighbors = pos.neighbors(data.moves, data.limits)
            if data.seats[pos] == "L":
                if all(data.seats[n] == "." or data.seats[n] == "L" for n in neighbors):
                    new_seats[pos] = "#"
            if data.seats[pos] == "#":
                if sum(data.seats[n] == "#" for n in neighbors) >= data.occupied_limit:
                    new_seats[pos] = "L"

        return new_seats

    def example_answer(self):
        return 37


class PartB(PartA):
    @staticmethod
    def step(data):
        new_seats = data.seats.mutable_copy()
        for x, y in itertools.product(range(data.limits[0][1]), range(data.limits[1][1])):
            pos = nographs.Position.at(x, y)
            if data.seats[pos] == "L":
                adjacent = 0
                for dir in data.moves:
                    neighbor = pos + dir
                    while neighbor.is_in_cuboid(data.limits):
                        if data.seats[neighbor] == "#":
                            adjacent += 1
                            break
                        if data.seats[neighbor] == "L":
                            break
                        neighbor = neighbor + dir
                if adjacent == 0:
                    new_seats[pos] = "#"
            if data.seats[pos] == "#":
                adjacent = 0
                for dir in data.moves:
                    neighbor = pos + dir
                    while neighbor.is_in_cuboid(data.limits):
                        if data.seats[neighbor] == "L":
                            break
                        if data.seats[neighbor] == "#":
                            adjacent += 1
                            break
                        neighbor = neighbor + dir
                if adjacent >= 5:
                    new_seats[pos] = "L"
        return new_seats

    def example_answer(self):
        return 26


Day.do_day(11, 2020, PartA, PartB)
