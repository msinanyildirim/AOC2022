def build_cave_grid(input_file_path):

    # Reading the input file
    with open(input_file_path, "r") as file:
        puzzle_input = file.read().splitlines()

    # For each line get a list of coordinates
    puzzle_input = [puzzle_line.split(" -> ") for puzzle_line in puzzle_input]

    # Initialize a grid of all air particles
    N = 1000
    cave_grid = [['.' for _ in range(N)] for _ in range(N)]

    maxy = 0 # Initialize the maxy as 0
    for puzzle_line in puzzle_input:
        # Get the initial point and mark it as rock
        startx, starty = puzzle_line[0].split(",")
        startx, starty = int(startx), int(starty)
        cave_grid[startx][starty] = "#"
        
        if starty > maxy: # Update maxy if a larger value is seen
            maxy = starty

        prevx, prevy = startx, starty
        for next_point in puzzle_line[1:]:
            # Get the next point
            nextx, nexty = next_point.split(",")
            nextx, nexty = int(nextx), int(nexty)
            
            if nexty > maxy: # Update maxy if a larger value is seen
                maxy = nexty

            if nextx == prevx:
                starty = min(prevy, nexty)
                endy = max(prevy, nexty)

                # If x values are same, fill rocks between the points vertically
                for curry in range(starty, endy+1):
                    cave_grid[nextx][curry] = "#"

            elif nexty == prevy:
                startx = min(prevx, nextx)
                endx = max(prevx, nextx)

                # If y values are same, fill rocks between the points horizontally
                for currx in range(startx, endx+1):
                    cave_grid[currx][nexty] = "#"

            prevx, prevy = nextx, nexty # Update previous point


    # Drawing the floor
    for tempx in range(N):
        cave_grid[tempx][maxy+2] = "#"

    return cave_grid


def simulate_sand(cave_grid, start_pos):
    sandx, sandy = start_pos[0], start_pos[1] # Initialize sand position

    num_row = len(cave_grid)
    num_col = len(cave_grid[0])

    while True:
        if sandy == num_col - 1: # If sand reached bottom, break the loop 
            return sandx, -1

        if cave_grid[sandx][sandy+1] == ".": # Checking if sand can go down 
            sandy += 1
            continue
        elif cave_grid[sandx-1][sandy+1] == ".": # Checking if sand can go down left 
            sandx -= 1
            sandy += 1
            continue
        elif cave_grid[sandx+1][sandy+1] == ".": # Checking if sand can go down right
            sandx += 1
            sandy += 1
            continue
        else:
            return sandx, sandy


if __name__ == "__main__":

    cave_grid = build_cave_grid("./input_14.txt")

    num_resting_sands = 0
    while True:
        finalx, finaly = simulate_sand(cave_grid, (500, 0))
        if finaly == -1:
            break
        elif finaly == 0: # If the sand source is blocked, the flow is stopped
            cave_grid[finalx][finaly] = "O"
            num_resting_sands += 1
            break
        else:
            cave_grid[finalx][finaly] = "O"
            num_resting_sands += 1

    print(num_resting_sands)
