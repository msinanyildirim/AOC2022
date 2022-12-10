with open("./input_10.txt", "r") as file:
    puzzle_input = file.read().splitlines()

# Function to determine if sprite coincides with curr
def is_coincide(curr_X, cycle_num):
    if (curr_X - ((cycle_num - 1) % 40))  in [-1,0,1]:
        return 1
    else:
        return 0

curr_X = 1
result = ""
cycle_num = 1

oper_to_func   = {"addx": lambda x,y: x+y , "noop": lambda x,y: x}
oper_to_cycles = {"addx": 2               , "noop": 1}

for curr_line in puzzle_input:
    # Getting the operation name
    operation = curr_line[:4]
    # Getting the append
    operand = int(curr_line[5:]) if curr_line[5:] != "" else ""

    for _ in range(oper_to_cycles[operation]):
        curr_pix = "#" if is_coincide(curr_X, cycle_num) else "."
        result += curr_pix
        if cycle_num % 40 == 0:
            result += "\n"

        cycle_num += 1
    else:
        curr_X = oper_to_func[operation](curr_X, operand)

print(result)

