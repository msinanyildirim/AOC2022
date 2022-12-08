# Reading the puzzle input
with open("./input_08.txt") as file:
    puzzle_input = file.read().splitlines()

num_row = len(puzzle_input)
num_col = len(puzzle_input[0])
tree_map =  [[]] * num_row

for i in range(num_row):
    tree_map[i] = [int(height) for height in list(puzzle_input[i])]

# Initializing all trees as invisible
visibility_map = [[0 for _ in range(num_col)] for _ in range(num_row)]

# For all rows check if current tree is visible from left
for i in range(num_row):
    max_till_now = -1
    for j in range(num_col):
        curr_height = tree_map[i][j]
        if visibility_map[i][j] == 1:
            max_till_now = max(max_till_now, curr_height)
            continue
        else:
            if curr_height > max_till_now:
                visibility_map[i][j] = 1
                max_till_now = curr_height

# For all rows check if current tree is visible from right
for i in range(num_row):
    max_till_now = -1
    for j in range(num_col-1, -1, -1):
        curr_height = tree_map[i][j]
        if visibility_map[i][j] == 1:
            max_till_now = max(max_till_now, curr_height)
            continue
        else:
            if curr_height > max_till_now:
                visibility_map[i][j] = 1
                max_till_now = curr_height

# For all columns check if current tree is visible from up
for j in range(num_col):
    max_till_now = -1
    for i in range(num_row):
        curr_height = tree_map[i][j]
        if visibility_map[i][j] == 1:
            max_till_now = max(max_till_now, curr_height)
            continue
        else:
            if curr_height > max_till_now:
                visibility_map[i][j] = 1
                max_till_now = curr_height

# For all columns check if current tree is visible from down
for j in range(num_col):
    max_till_now = -1
    for i in range(num_row-1, -1, -1):
        curr_height = tree_map[i][j]
        if visibility_map[i][j] == 1:
            max_till_now = max(max_till_now, curr_height)
            continue
        else:
            if curr_height > max_till_now:
                visibility_map[i][j] = 1
                max_till_now = curr_height

# Calculating # of trees visible from outside
final_result = sum([sum(row) for row in visibility_map])
print(f"There are this many visible trees: {final_result}")

