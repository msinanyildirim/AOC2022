import re


class BoardMap:
    def __init__(self, board_map):
        # Add trailing spaces to the lines that are shorter
        max_len = max([len(line) for line in board_map])
        board_map = [curr_line + " "*(max_len - len(curr_line)) for curr_line in board_map]

        # Add one space at the start and at the end of each row to cover the map with at least one layer of spaces
        board_map = [" " + curr_line + " " for curr_line in board_map]

        # Add a column of spaces at the top and bottom of the map
        first_line = " " * len(board_map[0])
        last_line = " " * len(board_map[-1])

        self.board_map = [first_line] + board_map + [last_line]

        # Finding the starting position
        start_col = self.board_map[1].index(".")
        self.pos = complex(1, start_col)

        # Starting direction is to the right
        self.dir = complex(0, 1)

    def pos_to_tile(self, input_pos):
        row_idx = int(input_pos.real)
        col_idx = int(input_pos.imag)
        return self.board_map[row_idx][col_idx]

    def move_one_step(self):
        next_pos = self.pos + self.dir
        next_tile = self.pos_to_tile(next_pos)

        # If next tile is space, find the position to wrap around to
        if next_tile == " ":
            wrap_dir = (-1) * self.dir
            wrap_pos = self.pos
            while True:
                next_pos = wrap_pos
                wrap_pos = next_pos + wrap_dir
                if self.pos_to_tile(wrap_pos) == " ":
                    break

            next_tile = self.pos_to_tile(next_pos)

        # Change the position and return true if movement can occur, otherwise do nothing and return False
        if next_tile == "#":
            return False
        elif next_tile == ".":
            self.pos = next_pos
            return True
        else:
            raise Exception(f"Next tile is {next_tile} which is never expected.")

    def move(self, num_steps):
        for _ in range(num_steps):
            has_moved = self.move_one_step()

            # If no movement has occurred, no need to try further
            if not has_moved:
                break

    def turn(self, turn_dir):
        if turn_dir == "R":
            self.dir = complex(0, -1) * self.dir
        elif turn_dir == "L":
            self.dir = complex(0, 1) * self.dir
        else:
            raise Exception(f"Turn direction must either be R or L but it is {turn_dir}.")

    def final_password(self):
        if self.dir == complex(0, 1):
            final_facing = 0
        elif self.dir == complex(1, 0):
            final_facing = 1
        elif self.dir == complex(0, -1):
            final_facing = 2
        elif self.dir == complex(-1, 0):
            final_facing = 3
        else:
            raise Exception(f"The direction is {self.dir} which is not to be expected.")

        password = 1000 * self.pos.real + 4 * self.pos.imag + final_facing
        password = int(password)
        return password


if __name__ == "__main__":
    with open("input_22.txt", "r") as file:
        puzzle_input = file.read().splitlines()

    instructions = puzzle_input[-1]
    instructions = re.split(r"([RL])", instructions)

    input_map = puzzle_input[:-2]
    board_map = BoardMap(input_map)

    for idx in range(len(instructions)):
        if idx % 2 == 0:
            curr_steps = int(instructions[idx])
            board_map.move(curr_steps)
        else:
            curr_turn_dir = instructions[idx]
            board_map.turn(curr_turn_dir)

    print(f"Final password is {board_map.final_password()}")
