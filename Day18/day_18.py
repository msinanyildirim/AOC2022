import numpy as np


class LavaDroplet:

    def __init__(self, drop_coordinates: list, dim=50):
        self.dim = dim
        self.state = np.zeros([self.dim] * 3, dtype=int)
        self.surface_area = 0

        for curr_drop_coordinate in drop_coordinates:
            self.add_drop(curr_drop_coordinate)

    def add_drop(self, drop_coordinate: tuple):

        assert self.state[drop_coordinate] != 1, f"You are trying to add a drop to the same position as another drop."

        self.state[drop_coordinate] = 1

        num_occupied_neighbors = self.get_num_occupied_neighbours(drop_coordinate)
        num_possible_neighbors = self.get_num_possible_neighbours(drop_coordinate)
        self.surface_area += num_possible_neighbors - 2 * num_occupied_neighbors

    def get_possible_neighbours(self, drop_coordinate: tuple):
        curr_x, curr_y, curr_z = drop_coordinate

        curr_neighbours = set()

        if curr_x - 1 >= 0:
            curr_neighbours.add((curr_x - 1, curr_y, curr_z))

        if curr_x + 1 < self.dim:
            curr_neighbours.add((curr_x + 1, curr_y, curr_z))

        if curr_y - 1 >= 0:
            curr_neighbours.add((curr_x, curr_y - 1, curr_z))

        if curr_y + 1 < self.dim:
            curr_neighbours.add((curr_x, curr_y + 1, curr_z))

        if curr_z - 1 >= 0:
            curr_neighbours.add((curr_x, curr_y, curr_z - 1))

        if curr_z + 1 < self.dim:
            curr_neighbours.add((curr_x, curr_y, curr_z + 1))

        return curr_neighbours

    def get_num_possible_neighbours(self, drop_coordinate: tuple):
        return len(self.get_possible_neighbours(drop_coordinate))

    def get_occupied_neighbours(self, drop_coordinate: tuple):
        curr_neighbours = self.get_possible_neighbours(drop_coordinate)

        occupied_neighbours = set()
        for curr_point in curr_neighbours:
            if self.state[curr_point] == 1:
                occupied_neighbours.add(curr_point)

        return occupied_neighbours

    def get_num_occupied_neighbours(self, drop_coordinate: tuple):
        return len(self.get_occupied_neighbours(drop_coordinate))


def read_puzzle(input_path: str):
    # Read the given text file line by line
    with open(input_path, "r") as file:
        puzzle_input = file.read().splitlines()

    # For each line, split by commas and get the point
    curr_coordinates = []
    for curr_line in puzzle_input:
        curr_x, curr_y, curr_z = curr_line.split(",")
        curr_x, curr_y, curr_z = int(curr_x), int(curr_y), int(curr_z)
        curr_point = (curr_x, curr_y, curr_z)
        curr_coordinates.append(curr_point)

    # Find the minimum for each coordinate
    all_x, all_y, all_z = zip(*curr_coordinates)
    min_x = min(all_x)
    min_y = min(all_y)
    min_z = min(all_z)

    # We want to shift the whole object such that min for each coordinate becomes 1
    norm_x = 1 - min_x
    norm_y = 1 - min_y
    norm_z = 1 - min_z

    # Apply the calculated shift
    curr_coordinates = [(curr_point[0]+norm_x, curr_point[1]+norm_y, curr_point[2]+norm_z)
                        for curr_point in curr_coordinates]

    # Find the maximum among all coordinates after the normalization shift
    all_x, all_y, all_z = zip(*curr_coordinates)
    max_dim = max(all_x + all_y + all_z)

    # Input dimensions should be 2 greater than max_dim such that there is empty space around the object
    input_dim = max_dim + 2

    return curr_coordinates, input_dim


if __name__ == "__main__":

    curr_coordinates, input_dim = read_puzzle("input_18.txt")

    lava_droplet = LavaDroplet(drop_coordinates=curr_coordinates, dim=input_dim)
    print(f"Result for part 1 is {lava_droplet.surface_area}")

    water_object = LavaDroplet([], dim=input_dim)
    new_points = {(0, 0, 0)}

    while len(new_points) > 0:

        for curr_point in new_points:
            water_object.add_drop(curr_point)

        prev_points = new_points
        new_points = set()

        for curr_point in prev_points:
            water_possible_points = water_object.get_possible_neighbours(curr_point)
            water_occupied_points = water_object.get_occupied_neighbours(curr_point)
            lava_droplet_points = lava_droplet.get_occupied_neighbours(curr_point)

            available_points = water_possible_points - water_occupied_points - lava_droplet_points
            new_points = new_points | available_points

    print(f"Result for part 2 is {water_object.surface_area}")
