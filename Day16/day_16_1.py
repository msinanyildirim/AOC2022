import itertools
import re

class Graph():
    def __init__(self):
        self.nodes = set()
        self.edges = dict()
        self.shortest_distances_cache = dict()
        
    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.add(node)
            self.edges[node] = set()

    def add_edge(self, from_node, to_node):
        if from_node not in self.nodes:
            self.add_node(from_node)

        if to_node not in self.nodes:
            self.add_node(to_node)

        self.edges[from_node].add(to_node)




    def shortest_distance(self, from_node, to_node):
        if from_node in self.shortest_distances_cache and to_node in self.shortest_distances_cache[from_node]:
            return self.shortest_distances_cache[from_node][to_node]

        assert from_node in self.nodes, f"{from_node=} is not in the graph"
        assert to_node in self.nodes, f"{to_node=} is not in the graph"

        if from_node == to_node:
            return 0

        possible_next_nodes = self.edges[from_node]

        if len(possible_next_nodes) == 0:
            return float("inf")
        
        min_distances = []
        for possible_next_node in possible_next_nodes:
            reduced_graph = Graph()
            for curr_node in self.edges:
                if curr_node == from_node:
                    continue
                else:
                    reduced_graph.add_node(curr_node)
                    curr_connections = self.edges[curr_node].copy()
                    curr_connections.discard(from_node)

                    for curr_edge_to_node in curr_connections:
                        reduced_graph.add_edge(curr_node, curr_edge_to_node)

            curr_possible_min = reduced_graph.shortest_distance(possible_next_node, to_node)
            min_distances.append(curr_possible_min)

        overall_min = min(min_distances) + 1
        
        if from_node in self.shortest_distances_cache:
            self.shortest_distances_cache[from_node][to_node] = overall_min
        else:
            self.shortest_distances_cache[from_node] = dict()
            self.shortest_distances_cache[from_node][to_node] = overall_min

        if to_node in self.shortest_distances_cache:
            self.shortest_distances_cache[to_node][from_node] = overall_min
        else:
            self.shortest_distances_cache[to_node] = dict()
            self.shortest_distances_cache[to_node][from_node] = overall_min

        return overall_min


def pressure_finder(tunnel_map, curr_node, nodes_to_visit, time_limit):

    if time_limit < 0:
        return 0

    if len(nodes_to_visit) == 0:
        return 0

    max_pressure = 0
    for next_node in nodes_to_visit:

        curr_pressure = 0
        curr_time = 0

        travel_time = tunnel_map.shortest_distance(curr_node, next_node)
        curr_time += travel_time + 1

        if curr_time < time_limit:
            # print(f"{nodes_to_visit=}")
            curr_pressure += nodes_to_visit[next_node] * (time_limit - curr_time)

            remaining_nodes = nodes_to_visit.copy()
            del remaining_nodes[next_node]

            new_time_limit = time_limit-curr_time

            curr_pressure += pressure_finder(tunnel_map, next_node, remaining_nodes, new_time_limit)

        if curr_pressure > max_pressure:
            max_pressure = curr_pressure

    return max_pressure


if __name__ == "__main__":

    with open("./input_16.txt", "r") as file:
        puzzle_lines = file.read().splitlines()

    non_zero_valves = {}
    tunnel_map = Graph()
    for curr_line in puzzle_lines:
        curr_line_matches = re.match(r"Valve ([A-Z]+) has flow rate=([\d]+); tunnel[s]? lead[s]? to valve[s]? ([A-Z\s,]+)", curr_line)
        from_node, node_rate, to_nodes = curr_line_matches.groups()

        to_nodes = to_nodes.split(", ")
        for curr_to_node in to_nodes:
            tunnel_map.add_edge(from_node, curr_to_node)

        if node_rate != "0":
            node_rate = int(node_rate)
            non_zero_valves[from_node] = node_rate

    time_limit = 30
    start_node = "AA"

    max_pressure = pressure_finder(tunnel_map, start_node, non_zero_valves, time_limit)
    print(max_pressure)

