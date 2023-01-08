import numpy as np
import scipy
import time


class ElfGroup:
    def __init__(self, map_input: list[str]):
        num_row = len(map_input)
        num_col = len(map_input[0])

        self.state = np.zeros((num_row, num_col), dtype=bool)

        for row_index in range(num_row):
            for col_index in range(num_col):
                curr_tile = map_input[row_index][col_index]
                if curr_tile == ".":
                    continue
                elif curr_tile == "#":
                    self.state[row_index][col_index] = True
                else:
                    raise Exception(f"The map must consist of # and . but this map has {curr_tile}")

        self.kernel = np.array([[2, 4, 8], [256, 1, 16], [128, 64, 32]])

        self.directions = {"N": (0, 1, 2, 3), "S": (0, 5, 6, 7), "E": (0, 3, 4, 5), "W": (0, 1, 7, 8)}
        self.dir_order = ["N", "S", "W", "E"]
        self.dir_to_dir = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}

    def unpad_state(self):
        while not np.any(self.state[0]):
            self.state = self.state[1:]

        while not np.any(self.state[-1]):
            self.state = self.state[:-1]

        while not np.any(self.state[:, 0]):
            self.state = self.state[:, 1:]

        while not np.any(self.state[:, -1]):
            self.state = self.state[:, :-1]

    def play_one_round(self):

        conv_result = scipy.signal.correlate2d(self.state, self.kernel)
        conv_result[conv_result % 2 == 0] = 0
        conv_result[conv_result == 1] = 0

        if conv_result[conv_result > 1].shape[0] == 0:
            return False

        new_pos_to_old = {}
        curr_elf_locations = conv_result.nonzero()
        for row_idx, col_idx in zip(*curr_elf_locations):
            curr_flag = conv_result[row_idx, col_idx]
            curr_flag = f"{curr_flag:09b}"
            curr_flag = curr_flag[::-1]
            for curr_dir in self.dir_order:
                curr_bits = [curr_flag[curr_bit_index] for curr_bit_index in self.directions[curr_dir]]
                curr_bits = "".join(curr_bits)
                can_move = "1000" == curr_bits
                if can_move:
                    pos_change = self.dir_to_dir[curr_dir]
                    new_row_idx, new_col_idx = row_idx + pos_change[0], col_idx + pos_change[1]
                    new_pos = (new_row_idx, new_col_idx)
                    if new_pos in new_pos_to_old:
                        del new_pos_to_old[new_pos]
                    else:
                        old_pos = (row_idx, col_idx)
                        new_pos_to_old[new_pos] = old_pos

                    break

        self.state = np.pad(self.state, 1)
        for new_pos, old_pos in new_pos_to_old.items():
            self.state[old_pos] = False
            self.state[new_pos] = True

        self.dir_order.append(self.dir_order.pop(0))
        self.unpad_state()
        return True

    def play_n_rounds(self, n):
        for _ in range(n):
            self.play_one_round()

    def get_empty_space(self):
        empty_tiles = self.state[self.state == False]
        empty_space = empty_tiles.shape[0]
        return empty_space

    def play_until_convergence(self):
        curr_round = 0
        while True:
            curr_flag = self.play_one_round()
            curr_round += 1
            if not curr_flag:
                break
        return curr_round


if __name__ == "__main__":
    with open("input_23.txt", "r") as file:
        puzzle_input = file.read().splitlines()

    elf_group = ElfGroup(puzzle_input)
    elf_group.play_n_rounds(10)

    print(f"After 10 rounds, number of empty tiles is {elf_group.get_empty_space()}")

    st = time.time()

    elf_group = ElfGroup(puzzle_input)
    num_rounds = elf_group.play_until_convergence()
    print(f"First round where the elves did not move was round {num_rounds}")

    et = time.time()
    print(f"Part 2 time: {et-st} seconds")
