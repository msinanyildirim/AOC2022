# Reading the puzzle input
with open("./input_08.txt") as file:
    puzzle_input = file.read().splitlines()

num_row = len(puzzle_input)
num_col = len(puzzle_input[0])
tree_map =  [[]] * num_row

for i in range(num_row):
    tree_map[i] = [int(height) for height in list(puzzle_input[i])]

# Going through all trees
max_score = 0
for i in range(num_row):
    for j in range(num_col):
        curr_height = tree_map[i][j]

        # Calculating # of trees seen to north
        for up_pos in range(i-1, -1, -1):
            if tree_map[up_pos][j] >= curr_height:
                up_score = i - up_pos 
                break
        else:
            up_score = i

        # Calculating # of trees seen to west
        for left_pos in range(j-1, -1, -1):
            if tree_map[i][left_pos] >= curr_height:
                left_score = j - left_pos 
                break
        else:
            left_score = j

        # Calculating # of trees seen to south
        for down_pos in range(i+1, num_row, +1):
            if tree_map[down_pos][j] >= curr_height:
                down_score = down_pos - i
                break
        else:
            down_score =  num_row -1 - i

        # Calculating # of trees seen to east
        for right_pos in range(j+1, num_col, +1):
            if tree_map[i][right_pos] >= curr_height:
                right_score = right_pos -j
                break
        else:
           right_score = num_col -1 - j

        # Calculating the scenic score for the current tree
        curr_score = left_score * right_score * up_score * down_score

        # Check if current score is maximum
        if curr_score > max_score:
            max_score = curr_score

print(f"Maximum scenic score is {max_score}")
