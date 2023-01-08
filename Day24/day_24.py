import numpy as np


class Blizzard:
    def __init__(self, row_idx: int, col_idx: int, direction: str, max_bound: int):
        self.row = row_idx
        self.col = col_idx

        if direction in ">v":
            self.dir = 1
            self.trigger = max_bound
            self.jump_to = 1
        elif direction in "<^":
            self.dir = -1
            self.trigger = 0
            self.jump_to = max_bound - 1
        else:
            raise Exception(f"A blizzard can have direction <>^v but {direction} was given")

    def get_pos(self):
        return self.row, self.col


class HorizontalBlizzard(Blizzard):
    def update_pos(self):
        self.col += self.dir
        if self.col == self.trigger:
            self.col = self.jump_to


class VerticalBlizzard(Blizzard):
    def update_pos(self):
        self.row += self.dir
        if self.row == self.trigger:
            self.row = self.jump_to


class Valley:
    def __init__(self, input_map: list[str]):
        self.num_row = len(input_map)
        self.num_col = len(input_map[0])

        self.blizzards = []

        for row_idx, curr_row in enumerate(input_map):
            for col_idx, curr_tile in enumerate(curr_row):
                if curr_tile in ".#":
                    continue
                elif curr_tile in "<>":
                    curr_blizzard = HorizontalBlizzard(row_idx, col_idx, curr_tile, self.num_col - 1)
                    self.blizzards.append(curr_blizzard)
                elif curr_tile in "^v":
                    curr_blizzard = VerticalBlizzard(row_idx, col_idx, curr_tile, self.num_row - 1)
                    self.blizzards.append(curr_blizzard)
                else:
                    raise Exception(f"The map should consist of .#<>^v but it has {curr_tile}")

    def update_valley(self):
        for curr_blizzard in self.blizzards:
            curr_blizzard.update_pos()

    def find_minimum_steps(self, start_pos, dest_pos):
        curr_possible_pos = set()
        curr_step = 0

        while True:
            prev_possible_pos = curr_possible_pos
            curr_possible_pos = set()

            self.update_valley()

            curr_valley = np.ones((self.num_row - 2, self.num_col - 2), dtype=int)
            curr_valley = np.pad(curr_valley, 1)

            for curr_blizzard in self.blizzards:
                curr_row, curr_col = curr_blizzard.get_pos()
                curr_valley[curr_row, curr_col] = 0

            if curr_valley[start_pos] == 1:
                curr_possible_pos.add(start_pos)

            for prev_pos in prev_possible_pos:
                prev_row, prev_col = prev_pos
                pos_to_check = [(prev_row,     prev_col),
                                (prev_row - 1, prev_col),
                                (prev_row,     prev_col - 1),
                                (prev_row + 1, prev_col),
                                (prev_row,     prev_col + 1)]
                for check_pos in pos_to_check:
                    if curr_valley[check_pos] == 1:
                        curr_possible_pos.add(check_pos)

            curr_step += 1

            if dest_pos in curr_possible_pos:
                self.update_valley()
                curr_step += 1
                break

        return curr_step


if __name__ == "__main__":
    with open("input_24.txt", "r") as file:
        puzzle_input = file.read().splitlines()

    my_valley = Valley(puzzle_input)
    num_row = len(puzzle_input)

    start_pos = (1, puzzle_input[0].index("."))
    dest_pos = (num_row - 2, puzzle_input[-1].index("."))

    min_steps_1 = my_valley.find_minimum_steps(start_pos, dest_pos)
    min_steps_2 = my_valley.find_minimum_steps(dest_pos, start_pos)
    min_steps_3 = my_valley.find_minimum_steps(start_pos, dest_pos)

    total_steps = min_steps_1 + min_steps_2 + min_steps_3

    print(f"Part 1: The valley can be traversed in {min_steps_1} steps")
    print(f"Part 2: The whole journey can be traversed in {total_steps} steps ")
