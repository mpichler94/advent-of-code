from utils.aoc_base import Day
import itertools
import re
from collections import namedtuple
import nographs as nog


Valve = namedtuple('Valve', ['name', 'flow', 'connections'])


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()
        data.valves = {}
        for i in range(0, len(lines), 1):
            line = lines[i].strip()
            match = re.match(r'Valve (.*?) has flow rate=(\d+); tunnels? leads? to valves? (.*)', line)

            connections = match.group(3).split(', ')
            data.valves[match.group(1)] = Valve(match.group(1), int(match.group(2)), connections)

        for name, valve in data.valves.items():
            con = []
            for connection in valve.connections:
                con.append(data.valves[connection])
            valve.connections.clear()
            for con1 in con:
                valve.connections.append(con1)

    def compute(self, data):
        return self.best_path(data.valves, 30)

    def best_path(self, valves, rem_time):
        max_flow = sum(valve.flow for valve in valves.values())
        closed_valves = [name for name, valve in valves.items() if valve.flow > 0]

        traversal = nog.TraversalShortestPaths(self.edges_function(valves, max_flow))
        for state in traversal.start_from(('AA', frozenset(closed_valves), 0)):
            pos, closed, flow = state
            if traversal.depth == rem_time or not closed:
                return max_flow * rem_time - traversal.distance

    @staticmethod
    def edges_function(valves, max_flow):
        def next_edges(state, _):
            pos, closed, flow = state

            if pos in closed:
                yield (pos, closed.difference({pos}), flow + valves[pos].flow), (max_flow - flow)
            for valve in valves[pos].connections:
                yield (valve.name, closed, flow), (max_flow - flow)

        return next_edges

    def example_answer(self):
        return 1651


class PartB(PartA):
    def compute(self, data):
        return self.best_path(data.valves, 26)

    def best_path(self, valves, rem_time):
        max_flow = sum(valve.flow for valve in valves.values())
        closed_valves = [name for name, valve in valves.items() if valve.flow > 0]

        traversal = nog.TraversalShortestPaths(self.edges_function(valves, max_flow))
        for state in traversal.start_from(('AA', 'AA', frozenset(closed_valves), 0)):
            pos1, pos2, closed, flow = state
            if traversal.depth == rem_time or not closed:
                return max_flow * rem_time - traversal.distance

    def edges_function(self, valves, max_flow):
        next_edges = PartA.edges_function(valves, max_flow)

        def next_edges_b(state, _):
            pos1, pos2, closed, flow = state

            for state1, state2 in itertools.product(next_edges((pos1, closed, flow), _), next_edges((pos2, closed, flow), _)):
                (pos1, closed1, flow1), weight1 = state1
                (pos2, closed2, flow2), weight2 = state2

                if state1[0] != state2[0] or closed1 == closed:
                    yield (pos1, pos2, closed1.intersection(closed2), flow1 + flow2 - flow), weight1

        return next_edges_b

    def example_answer(self):
        return 1707


Day.do_day(16, 2022, PartA, PartB)
