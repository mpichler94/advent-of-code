from utils.aoc_base import Day
import re
from collections import namedtuple

Sensor = namedtuple('Sensor', ['pos', 'distance', 'beacon'])


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.sensors = []
        for i in range(len(lines)):
            line = lines[i].strip()
            match = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)
            pos = [int(match.group(1)), int(match.group(2))]
            beacon = [int(match.group(3)), int(match.group(4))]
            distance = abs(pos[0] - beacon[0]) + abs(pos[1] - beacon[1])
            data.sensors.append(Sensor(pos, distance, beacon))

    def compute(self, data):
        target_row = 2000000 if len(data.sensors) != 14 else 10
        num_covered = self.covered_tiles(data.sensors, target_row)
        return num_covered

    @staticmethod
    def covered_tiles(sensors, target_row):
        row = set()
        beacons = set()

        for sensor in sensors:
            if sensor.beacon[1] == target_row:
                beacons.add(sensor.beacon[0])

            y_distance = abs(target_row - sensor.pos[1])
            x_distance = sensor.distance - y_distance
            if x_distance < 0:
                continue

            x_min = sensor.pos[0] - x_distance
            x_max = sensor.pos[0] + x_distance + 1

            for x in range(x_min, x_max):
                row.add(x)

        for beacon in beacons:
            row.remove(beacon)

        return len(row)

    def example_answer(self):
        return 26


class PartB(PartA):
    def compute(self, data):
        x, y = self.free_tile(data.sensors)
        return x * 4000000 + y

    @staticmethod
    def free_tile(sensors):
        max = 4000000

        beacons = ((sensor.beacon[0], sensor.beacon[1]) for sensor in sensors)

        for sensor in sensors:
            top_y = sensor.pos[1] + sensor.distance - 1
            bottom_y = sensor.pos[1] - sensor.distance - 1

            for i in range(sensor.distance):
                for x, y in (
                        (sensor.pos[0] + i, top_y - i),
                        (sensor.pos[0] - i, top_y - i),
                        (sensor.pos[0] + i, bottom_y + i),
                        (sensor.pos[0] - i, bottom_y + i),
                ):
                    if x < 0 or y < 0 or x > max or y > max or (x, y) in beacons:
                        continue

                    for sensor2 in sensors:
                        s_dist = abs(sensor2.pos[0] - x) + abs(sensor2.pos[1] - y)
                        if s_dist <= sensor2.distance:
                            break
                    else:
                        return x, y

    def example_answer(self):
        return 56000011


Day.do_day(15, 2022, PartA, PartB)
