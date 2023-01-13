from utils.aoc_base import Day
import networkx as net


class PartA(Day):
    def parse(self, text, data):
        data.graph = net.Graph()
        edges = [tuple(edge.split('-')) for edge in text.splitlines()]
        data.graph.add_edges_from(edges)

    def compute(self, data):
        return self.explore_neighbors(data.graph, 'start', 0, [], self.can_visit)

    @staticmethod
    def can_visit(node, visited_small_caves):
        return node not in visited_small_caves

    def explore_neighbors(self, graph, node, num_paths, visited_small_caves, can_visit):
        if not can_visit(node, visited_small_caves):
            return num_paths
        if node == node.lower():    # small cave
            visited_small_caves.append(node)
        if node == "end":           # we do not leave the end cave
            return num_paths + 1

        for neighbor in graph.adj[node]:
            num_paths = self.explore_neighbors(graph, neighbor, num_paths, list(visited_small_caves), can_visit)

        return num_paths

    def example_answer(self):
        return 10


class PartB(PartA):
    @staticmethod
    def can_visit(node, visited_small_caves):
        if node == node.lower():
            counts = {key: visited_small_caves.count(key) for key in visited_small_caves}
            if node == 'start' and 'start' in counts:   # start can only be visited once
                return False
            double_visit = any(v == 2 for v in counts.values())
            if double_visit:        # did we already visit a small cave twice
                return node not in counts   # did we already visit the node
        return True

    def example_answer(self):
        return 36


Day.do_day(12, 2021, PartA, PartB)
