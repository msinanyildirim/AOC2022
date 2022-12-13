from string import ascii_lowercase as lowercase_letters


def read_maps(puzzle_input):
    height_map = []

    for i, line in enumerate(puzzle_input):
        curr_line_heights = []

        for j, curr_letter in enumerate(list(line)):
            if curr_letter == "S":
                curr_height = 0
                start_pos = (i,j)
            elif curr_letter == "E":
                curr_height = 25
                final_dest = (i,j)
            elif curr_letter in lowercase_letters:
                curr_height = lowercase_letters.index(curr_letter)
            else:
                raise Exception(f"{curr_letter} is unexpected in the map.")

            curr_line_heights.append(curr_height)

        height_map.append(curr_line_heights)

    return start_pos, final_dest, height_map


def update_point(pos, height_map, steps_map):
    i,j = pos

    num_row = len(height_map)
    num_col = len(height_map[0])

    flag = 0
    if steps_map[i][j] >= 0:
        new_steps = steps_map[i][j]
    else:
        new_steps = 999999999999999999999

    for di, dj in [(1,0), (-1,0), (0,1), (0,-1)]:
        k = i + di
        l = j + dj

        if k<0 or k>=num_row:
            continue
        if l<0 or l>=num_col:
            continue

        if height_map[k][l] < height_map[i][j] - 1:
            continue

        if steps_map[k][l] != -1 and steps_map[k][l] + 1 < new_steps:
            flag = 1
            new_steps = steps_map[k][l] + 1

    return flag, new_steps


def find_shortest(start_pos, final_dest, height_map):

    num_row = len(height_map)
    num_col = len(height_map[0])

    steps_map = []
    for i in range(num_row):
        curr_steps_row = []
        for j in range(num_col):
            curr_steps_row.append(-1)

        steps_map.append(curr_steps_row)

    curr_added = [start_pos]
    steps_map[start_pos[0]][start_pos[1]] = 0

    while len(curr_added) > 0:

        next_added =[]

        for i,j in curr_added:

            for di, dj in [(1,0), (-1,0), (0,1), (0,-1)]:
                k = i + di
                l = j + dj

                if k<0 or k>=num_row:
                    continue
                if l<0 or l>=num_col:
                    continue

                flag, new_steps = update_point((k,l), height_map, steps_map)
                if flag:
                    steps_map[k][l] = new_steps
                    next_added.append((k,l))

        curr_added = next_added

    return steps_map[final_dest[0]][final_dest[1]]

if __name__ == "__main__":

    with open("./input_12.txt", "r") as file:
        puzzle_input = file.read().splitlines()

    start_pos, final_dest, height_map = read_maps(puzzle_input)

    final_result = find_shortest(start_pos, final_dest, height_map)

    print(final_result)
