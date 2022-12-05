import re

with open('./input_05.txt', 'r') as file:
    puzzle_input = file.read().splitlines()

# Separating the first and second part of the puzzle inpur
separation_index = puzzle_input.index('')

start_state_string = puzzle_input[:separation_index]
start_state_string.reverse()

all_instructions = puzzle_input[separation_index+1:]

# Get the number of towers
tower_labels = re.findall(r' [0-9]+ ', start_state_string[0])

# Read in the current state of the crates
curr_state = [[] for _ in tower_labels]

for i in range(1, len(curr_state)):
    curr_line = start_state_string[i]

    for m in re.finditer('\[[A-Z]\]', curr_line):
        start_pos = m.start()

        curr_state[start_pos//4].append(curr_line[start_pos+1])

# Apply the crane instructions
for curr_instruction in all_instructions:
    [_, num_crates, _, from_tower, _, to_tower] = curr_instruction.split(' ')

    num_crates = int(num_crates)
    from_tower = int(from_tower) - 1 # Subtract 1 because indices start from 0
    to_tower = int(to_tower) - 1

    for _ in range(num_crates):
        curr_state[to_tower].append(curr_state[from_tower].pop())

final_answer =  ''.join([tower_content[-1] for tower_content in curr_state])
print(f"The final answer to part 1 is {final_answer}")


