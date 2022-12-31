from collections import deque
import time


class Blueprint:
    def __init__(self, robot_costs: list[tuple[int, ...]]):
        # Checking to make sure each robot cost has number-of-metal-types elements
        self.num_robot_types = len(robot_costs)
        for curr_robot_cost in robot_costs:
            curr_num_metal_types = len(curr_robot_cost)
            assert curr_num_metal_types == self.num_robot_types, f"Each robot cost should give the cost for all metal types"

        # Assigning the costs
        self.robot_costs = robot_costs

        # Finding the maximum number of metals that can be spent in one minute, more than this cannot be spent
        self.metal_bounds = list(map(max, list(zip(*self.robot_costs))))

        # For the last robot, i.e. geode robot for our case, we should not have a maximum bound
        self.metal_bounds[-1] = float("inf")

    def can_buy(self, curr_metals: tuple[int, ...], robot_index: int):
        for elem1, elem2 in zip(curr_metals, self.robot_costs[robot_index]):
            if elem2 > elem1:
                return False

        return True

    def buy_robot(self, curr_metals: tuple[int, ...], robot_index: int):
        new_metals = [0] * self.num_robot_types
        for i in range(self.num_robot_types):
            new_metals[i] = curr_metals[i] - self.robot_costs[robot_index][i]
        new_metals = tuple(new_metals)
        return new_metals

    def metal_production(self, curr_robots: tuple[int, ...], curr_metals: tuple[int, ...]):
        result_metals = [0] * self.num_robot_types
        for i in range(self.num_robot_types):
            result_metals[i] = curr_robots[i] + curr_metals[i]
        result_metals = tuple(result_metals)
        return result_metals

    def reduce_metals(self, curr_metals: tuple[int, ...], curr_robots: tuple[int, ...], time_left: int):
        new_metals = list(curr_metals)
        for i in range(self.num_robot_types - 1):

            # For the current round, build the robot and for remaining t-1 rounds, gain from robots and still build
            curr_possible_max = (time_left - 1) * (self.metal_bounds[i] - curr_robots[i]) + self.metal_bounds[i]

            # More metals than this can never be spent, so we can discard them
            if new_metals[i] > curr_possible_max:
                new_metals[i] = curr_possible_max

        new_metals = tuple(new_metals)
        return new_metals

    def find_max_geode(self, start_metals, start_robots, start_time_left):

        start_state = (start_metals, start_robots, start_time_left)

        states_queue = deque()
        states_queue.append(start_state)

        max_geode_seen = start_metals[-1]

        seen_states = set()

        while len(states_queue) > 0:
            # print(len(states_queue))
            curr_state = states_queue.popleft()
            # print(curr_state)
            curr_metals, curr_robots, curr_time_left = curr_state

            # If this state is out of time, just check the number of geodes and move on
            if curr_time_left == 2:
                curr_geodes = curr_metals[-1]
                curr_geode_robots = curr_robots[-1]
                extra_geode_robot = 1 if self.can_buy(curr_metals, -1) else 0
                curr_max_geodes = curr_geodes + 2 * curr_geode_robots + extra_geode_robot
                max_geode_seen = max(max_geode_seen, curr_max_geodes)
                continue

            # If this state is seen, move on. If not seen, add it to the seen states and then process it
            curr_state = (curr_metals, curr_robots, curr_time_left)
            if curr_state in seen_states:
                continue
            seen_states.add(curr_state)

            # First adding the next states where a new robot is built
            for i in range(self.num_robot_types):
                if (curr_robots[i] < self.metal_bounds[i]) and self.can_buy(curr_metals, i):
                    new_metals = self.metal_production(curr_robots, curr_metals)
                    new_metals = self.buy_robot(new_metals, i)

                    new_robots = list(curr_robots)
                    new_robots[i] += 1
                    new_robots = tuple(new_robots)

                    # Reducing the current metals if we cannot possibly spend all
                    new_metals = self.reduce_metals(new_metals, new_robots, curr_time_left - 1)

                    new_state = (new_metals, new_robots, curr_time_left - 1)

                    states_queue.append(new_state)

            # Checking the case where no robot is built
            new_metals = self.metal_production(curr_robots, curr_metals)
            new_robots = curr_robots

            # Reducing the current metals if we cannot possibly spend all
            new_metals = self.reduce_metals(new_metals, new_robots, curr_time_left - 1)

            new_state = (new_metals, new_robots, curr_time_left - 1)
            states_queue.append(new_state)

        return max_geode_seen


if __name__ == "__main__":

    with open("input_19.txt", "r") as file:
        puzzle_lines = file.read().splitlines()

    blueprints = []
    for curr_line in puzzle_lines:
        curr_input = curr_line.split()
        curr_costs = [(int(curr_input[6]), 0, 0, 0),
                      (int(curr_input[12]), 0, 0, 0),
                      (int(curr_input[18]), int(curr_input[21]), 0, 0),
                      (int(curr_input[27]), 0, int(curr_input[30]), 0)]
        blueprints.append(Blueprint(curr_costs))

    # Part 1
    start_metals = (0, 0, 0, 0)
    start_robots = (1, 0, 0, 0)
    start_time_left = 24

    st = time.time()
    final_result = 0
    for idx, curr_blueprint in enumerate(blueprints):
        blueprint_id = (idx + 1)
        curr_max_geodes = curr_blueprint.find_max_geode(start_metals, start_robots, start_time_left)
        final_result += blueprint_id * curr_max_geodes

    print(f"Part 1 result is {final_result}")

    et = time.time()
    elapsed_time = et - st
    print(f'Part 1 took {elapsed_time} seconds')

    # Part 2
    start_metals = (0, 0, 0, 0)
    start_robots = (1, 0, 0, 0)
    start_time_left = 32

    st = time.time()
    final_result = 1
    for curr_blueprint in blueprints[:3]:
        curr_max_geodes = curr_blueprint.find_max_geode(start_metals, start_robots, start_time_left)
        final_result *= curr_max_geodes

    print(f"Part 2 result is {final_result}")

    et = time.time()
    elapsed_time = et - st
    print(f'Part 2 took {elapsed_time} seconds')
