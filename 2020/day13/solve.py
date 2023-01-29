import itertools
from functools import reduce
from operator import mul
from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        timestamp, busses = text.splitlines()
        data.timestamp = int(timestamp)
        data.busses = [int(bus) for bus in busses.split(",") if bus != "x"]
        data.diffs = []
        for i, bus in enumerate(busses.split(",")):
            if bus != "x":
                data.diffs.append(i)

    def compute(self, data):
        times = []
        for bus in data.busses:
            for fac in itertools.count(1):
                prod = bus * fac
                if prod >= data.timestamp:
                    times.append((bus, prod))
                    break

        times.sort(key=lambda x: x[1])
        first = times[0]
        return first[0] * (first[1] - data.timestamp)

    def example_answer(self):
        return 295


class PartB(PartA):
    def compute(self, data):
        # chinese remainder theorem
        n = reduce(mul, data.busses)

        x = 0
        for i, bus in enumerate(data.busses):
            y = n // bus
            z = pow(y, -1, bus)
            x += (-data.diffs[i] % bus) * y * z

        return x % n

    def example_answer(self):
        return 1068781


Day.do_day(13, 2020, PartA, PartB)
