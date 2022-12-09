# Function to return the sign of a scalar
def sign(x):
    if x > 0 :
        return 1
    elif x < 0:
        return -1
    else:
        return 0

# Function to calculate new position if moved by step from init_pos
def move_step(init_pos, step):
    result = [init_pos[0] + step[0], init_pos[1] + step[1]]
    return result

# Function to calculate the squared distance between two points
def dist_sq(head_pos, tail_pos):
    distance_squared = (head_pos[0] - tail_pos[0])**2 +  (head_pos[1]-tail_pos[1])**2
    return distance_squared

# Function which can update a knot according to the given rules
def update_knot(head_pos, tail_pos):
    distance_squared = dist_sq(head_pos, tail_pos)

    # Distance must be one of these, otherwise we must have done something wrong until now
    assert distance_squared in [0,1,2,4,5,8] , f"The {distance_squared=} between {head_pos=} and {tail_pos=} is something different than 0,1,2,4 or 5."

    # If squared disstance is 4 or 5 we, can update it, otherwise no need to update since the point are touching
    if distance_squared in [4,5,8]:
        x_sign = sign(head_pos[0] - tail_pos[0])
        y_sign = sign(head_pos[1] - tail_pos[1])
        tail_pos[0], tail_pos[1] = tail_pos[0] + x_sign, tail_pos[1] + y_sign
    return tail_pos

# Reading in the input
with open("./input_09.txt", "r") as file:
    puzzle_input = file.read().splitlines()

# Initializing the positions of head and all knots
N = 10 #Length of the rope
curr_state = [[0,0] for _ in range(N)]

# Dictionary that transforms letters into steps
dir_to_step = {"L": [-1,0], "R":[1,0] , "U":[0,1], "D":[0,-1]}

# Matrix keeping track of where the tail has been
visited_grid = [[0 for _ in range(1000) ] for _ in range(1000)]
tail_pos = curr_state[-1]
visited_grid[tail_pos[0]][tail_pos[1]] = 1

for move in puzzle_input:
    # Getting the direction and amount for the current move
    [move_dir, move_amount] = move.split(" ")
    curr_step = dir_to_step[move_dir]

    for _ in range(int(move_amount)):
        # Update the head and all the other knots
        curr_state[0] = move_step(curr_state[0], curr_step)
        for j in range(1,N):
            curr_state[j] = update_knot(curr_state[j-1], curr_state[j])

        # Update the history of tail pos
        tail_pos = curr_state[-1]
        visited_grid[tail_pos[0]][tail_pos[1]] = 1

# Getting number of positions where the tail has been
final_result = sum(sum(temp) for temp in visited_grid)
print(f"Final result for part 2 is {final_result}")        
