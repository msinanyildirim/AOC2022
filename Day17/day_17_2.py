import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y

        new_point = Point(new_x, new_y)
        return new_point


class BaseRock:
    def __init__(self):
        self.particles = []

    def move(self, move_dir: Point):
        new_particles = []
        for curr_particle in self.particles:
            new_particle_pos = curr_particle + move_dir
            new_particles.append(new_particle_pos)
        self.particles = new_particles


class HorizontalRock(BaseRock):
    def __init__(self, init_pos):
        super().__init__()
        init_shape = [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)]
        self.particles = [shape_point + init_pos for shape_point in init_shape]


class PlusRock(BaseRock):
    def __init__(self, init_pos):
        super().__init__()
        init_shape = [Point(0, 1), Point(1, 0), Point(1, 1), Point(2, 1), Point(1, 2)]
        self.particles = [shape_point + init_pos for shape_point in init_shape]


class ReverseLRock(BaseRock):
    def __init__(self, init_pos):
        super().__init__()
        init_shape = [Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2)]
        self.particles = [shape_point + init_pos for shape_point in init_shape]


class VerticalRock(BaseRock):
    def __init__(self, init_pos):
        super().__init__()
        init_shape = [Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)]
        self.particles = [shape_point + init_pos for shape_point in init_shape]


class BoxRock(BaseRock):
    def __init__(self, init_pos):
        super().__init__()
        init_shape = [Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)]
        self.particles = [shape_point + init_pos for shape_point in init_shape]


class Chamber:

    def __init__(self, width, jet_pattern):
        self.width = width
        self.state = np.ones([width, 1], dtype=int)
        self.height = 0
        self.possible_rocks = [HorizontalRock, PlusRock, ReverseLRock, VerticalRock, BoxRock]
        self.num_rocks = len(self.possible_rocks)
        self.curr_rock = None
        self.curr_rock_index = 0
        self.curr_jet_index = 0
        assert all(curr_char in "<>" for curr_char in jet_pattern), f"Jet pattern should only contain < or >"
        self.jet_pattern = jet_pattern
        self.num_jets = len(self.jet_pattern)
        self.previous_states = {}
        self.repeat_pattern = None
        self.append_state()

    def add_new_rock(self):
        assert isinstance(self.curr_rock, type(None)), f"A rock is trying to be added when there already is an active rock"
        new_rock_type = self.possible_rocks[self.curr_rock_index]
        new_rock_pos = Point(2, self.height + 4)
        self.curr_rock = new_rock_type(new_rock_pos)
        self.curr_rock_index += 1
        self.curr_rock_index %= self.num_rocks

    def is_rock_movable(self, move_dir=Point(0, -1)):
        for curr_particle in self.curr_rock.particles:
            new_pos = curr_particle + move_dir

            if new_pos.x < 0 or new_pos.x >= self.width:
                return False

            if self.state[new_pos.x][new_pos.y] == 1:
                return False

        else:
            return True

    def move_curr_rock(self, move_dir=Point(0, -1)):
        assert self.is_rock_movable(move_dir=move_dir), f"Trying to move the rock in an impossible position"
        self.curr_rock.move(move_dir)

    def jet_push_curr_rock(self):
        curr_jet_type = self.jet_pattern[self.curr_jet_index]
        curr_push_dir = Point(1, 0) if curr_jet_type == ">" else Point(-1, 0)
        if self.is_rock_movable(curr_push_dir):
            self.move_curr_rock(curr_push_dir)

        self.curr_jet_index += 1
        self.curr_jet_index %= self.num_jets

    def update_height(self):
        _, state_y = self.state.shape

        for curr_y in range(state_y - 1, -1, -1):
            curr_sum = self.state[:, curr_y].sum()
            if curr_sum > 0:
                self.height = curr_y
                return curr_y

    def finalize_curr_rock(self):
        for curr_particle in self.curr_rock.particles:
            curr_x, curr_y = curr_particle.x, curr_particle.y
            self.state[curr_x][curr_y] = 1

        self.curr_rock = None
        self.update_height()
        self.append_state()

    def append_state(self):
        curr_diff = 10 - (self.state.shape[1] - self.height)
        self.state = np.append(self.state, np.zeros([self.width, curr_diff], dtype=int), axis=1)

    def play_through(self, num_rounds: int):
        for curr_round in range(1, num_rounds + 1):
            self.add_new_rock()

            while True:
                self.jet_push_curr_rock()

                if self.is_rock_movable():
                    self.move_curr_rock()
                else:
                    self.finalize_curr_rock()
                    break

            if not isinstance(self.repeat_pattern, type(None)):
                rock_diff = self.repeat_pattern[0]
                height_diff = self.repeat_pattern[1]
                if (num_rounds - curr_round) % rock_diff == 0:
                    self.height += ((num_rounds - curr_round) // rock_diff) * height_diff
                    break
            else:
                self.save_curr_state(curr_round)

    def hash_chamber_state(self):
        lower_limit = 0
        for curr_y in range(self.height, -1, -1):
            curr_portion = self.state[:, curr_y:self.height+1]
            curr_col_sums = curr_portion.sum(axis=1)
            if 0 not in curr_col_sums:
                lower_limit = curr_y
                break

        result_string = ""
        for curr_y in range(self.height, lower_limit - 1, -1):
            curr_line = "".join(self.state[:, curr_y].astype(int).astype(str))
            result_string += curr_line
        return result_string

    def save_curr_state(self, round_index):
        curr_state = self.hash_chamber_state()
        curr_situation = (self.curr_rock_index, self.curr_jet_index, curr_state)

        if curr_situation in self.previous_states:
            rock_diff = round_index - self.previous_states[curr_situation][0]
            height_diff = self.height - self.previous_states[curr_situation][1]
            print(f"Found a pattern with {rock_diff=} and {height_diff=}")
            self.repeat_pattern = (rock_diff, height_diff)
        else:
            self.previous_states[curr_situation] = (round_index, self.height)


if __name__ == "__main__":
    with open("./input_17.txt", "r") as file:
        puzzle_input = file.read().splitlines()[0]

    my_chamber = Chamber(7, puzzle_input)
    num_rounds = 1000000000000
    my_chamber.play_through(num_rounds)
    print(f"After {num_rounds} rounds, the tower has a height of {my_chamber.height}")
