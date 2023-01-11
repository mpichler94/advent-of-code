import re
import numpy as np
import nographs

from utils.aoc_base import Day


class Blueprint:
    def __init__(self, id, costs):
        # ore, clay, obsidian, geode
        self.id = id
        self.costs = costs

    @staticmethod
    def from_string(str):
        match = re.match(r'Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.', str)
        id = int(match.group(1))
        ore_robot_cost = int(match.group(2))
        clay_robot_cost = int(match.group(3))
        obsidian_robot_ore_cost = int(match.group(4))
        obsidian_robot_clay_cost = int(match.group(5))
        geode_robot_ore_cost = int(match.group(6))
        geode_robot_obsidian_cost = int(match.group(7))
        costs = [(ore_robot_cost, 0, 0, 0),
                 (clay_robot_cost, 0, 0, 0),
                 (obsidian_robot_ore_cost, obsidian_robot_clay_cost, 0, 0),
                 (geode_robot_ore_cost, 0, geode_robot_obsidian_cost, 0)]

        return Blueprint(id, costs)

    def produce(self, minutes):
        def next_edges(state, traversal):
            materials, producing = state
            minutes_remaining = minutes - traversal.depth
            if minutes_remaining == 1:
                return

            new_materials = tuple(sum(x) for x in zip(materials, producing))
            robots_build = 0
            for robot_id in range(4):
                if robot_id < 3 and producing[robot_id] >= max_robots[robot_id]:
                    continue
                if all(cost <= material for cost, material in zip(self.costs[robot_id], materials)):
                    robots_build += 1
                    yield (tuple(material - cost for material, cost in zip(new_materials, self.costs[robot_id])), tuple(x + 1 if i == robot_id else x for i, x in enumerate(producing))), 0 if robot_id == 3 else minutes_remaining

            if robots_build == 4:
                return

            max_materials = tuple(material + production * minutes_remaining for material, production in zip(new_materials, producing))
            robots_buildable = 0
            for robot_id in range(4):
                if all(cost <= material for cost, material in zip(self.costs[robot_id], max_materials)):
                    robots_buildable += 1

            if robots_buildable == 0:
                return

            yield (new_materials, producing), minutes_remaining

        max_robots = tuple([max(self.costs[r][m] for r in range(4)) for m in range(4)])
        traversal = nographs.TraversalShortestPaths(next_edges)
        for state in traversal.start_from(((0, 0, 0, 0), (1, 0, 0, 0))):
            materials, produce = state
            if traversal.depth == minutes - 1:
                return materials[-1] + produce[-1]

        raise RuntimeError('no solution found')


class PartA(Day):
    def parse(self, text: str, data):
        lines = text.splitlines()
        data.blueprints = [Blueprint.from_string(str) for str in lines]

    def compute(self, data):
        quality_levels = []
        for blueprint in data.blueprints:
            quality_levels.append(blueprint.produce(24) * blueprint.id)

        return sum(quality_levels)

    def example_answer(self):
        return 33

    def example_input(self):
        return '''
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''


class PartB(PartA):
    def compute(self, data):
        geodes = []
        for i in range(min(3, len(data.blueprints))):
            blueprint = data.blueprints[i]
            geodes.append(blueprint.produce(32))

        return int(np.product(geodes))

    def example_answer(self):
        return 3472


Day.do_day(19, 2022, PartA, PartB)
