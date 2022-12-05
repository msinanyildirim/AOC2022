import re

with open('./input_05.txt', 'r') as file:
    puzzle_input = file.read().splitlines()

# Separating the first and second part of the puzzle inpur
separation_index = puzzle_input.index('')

start_state_string = puzzle_input[:separation_index]
start_state_string.reverse()

input_motions = puzzle_input[separation_index+1:]

# Get the number of towers
tower_labels = re.findall(r' [0-9]+ ', start_state_string[0])

curr_state = [[] for _ in tower_labels]

for i in range(1, len(curr_state)):
    curr_line = start_state_string[i]
    
    for m in re.finditer('\[[A-Z]\]', curr_line):
        start_pos = m.start()

        curr_state[start_pos//4].append(curr_line[start_pos+1])

print(curr_state)
