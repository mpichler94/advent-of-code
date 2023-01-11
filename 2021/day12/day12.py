import networkx as net


def read_input():
    file = open('day12/input.txt', encoding='utf8')
    data = file.read().splitlines()
    file.close()

    graph = net.Graph()

    edges = []
    for edge in data:
        edges.append(tuple(edge.split('-')))

    graph.add_edges_from(edges)

    return graph


def part_a(graph):
    num_paths = explore_neighbors(graph, 'start', 0, [], can_visit_a)
    print(f'[a] {num_paths} paths through the cave system')


def explore_neighbors(graph, node, num_paths, visited_small_caves, can_visit):
    if not can_visit(node, visited_small_caves):
        return num_paths
    if node == node.lower():    # small cave
        visited_small_caves.append(node)
    if node == "end":           # we do not leave the end cave
        return num_paths + 1

    for neighbor in graph.adj[node]:
        num_paths = explore_neighbors(graph, neighbor, num_paths, list(visited_small_caves), can_visit)

    return num_paths


def part_b(graph):
    num_paths = explore_neighbors(graph, 'start', 0, [], can_visit_b)
    print(f'[b] {num_paths} paths through the cave system')


def can_visit_a(node, visited_small_caves):
    if node in visited_small_caves:     # small caves can only be visited once
        return False
    return True


def can_visit_b(node, visited_small_caves):
    if node == node.lower():
        counts = {key: visited_small_caves.count(key) for key in visited_small_caves}
        if node == 'start' and 'start' in counts:   # start can only be visited once
            return False
        double_visit = any(v == 2 for v in counts.values())
        if double_visit:        # did we already visit a small cave twice
            if node in counts:  # did we already visit the node
                return False
            else:
                return True

    return True


def main():
    graph = read_input()
    part_a(graph)
    part_b(graph)


if __name__ == '__main__':
    main()
