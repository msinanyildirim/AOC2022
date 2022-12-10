with open("./input_10.txt", "r") as file:
    puzzle_input = file.read().splitlines()

curr_X = 1
result = 0
cycle_num = 1

oper_to_func   = {"addx": lambda x,y: x+y , "noop": lambda x,y: x}
oper_to_cycles = {"addx": 2,                "noop": 1}

for curr_line in puzzle_input:
    # Getting the operation name
    operation = curr_line[:4]
    # Getting the addend
    operand = int(curr_line[5:]) if curr_line[5:] != "" else ""

    for _ in range(oper_to_cycles[operation]):
        if cycle_num % 40 == 20:
            result += (curr_X * cycle_num)

        cycle_num += 1
    else:
        curr_X = oper_to_func[operation](curr_X, operand)

print(f"Final result for part 1 is {result}")
