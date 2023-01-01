def solve_monkey(monkey_name):
    curr_operation = monkeys[monkey_name]

    if len(curr_operation) == 1:
        return int(curr_operation[0])
    elif len(curr_operation) == 3:
        monkey1 = solve_monkey(curr_operation[0])
        math_operation = curr_operation[1]
        monkey2 = solve_monkey(curr_operation[2])
        curr_result = eval(f"{monkey1} {math_operation} {monkey2}")
        monkeys[monkey_name] = curr_result
        return curr_result
    else:
        raise Exception(f"{monkey_name} has unexpected length")


if __name__ == "__main__":
    with open("input_21.txt", "r") as file:
        puzzle_input = file.read().splitlines()

    monkeys = [curr_line.split() for curr_line in puzzle_input]
    monkeys = {monkey[0][:-1]: monkey[1:] for monkey in monkeys}

    result = solve_monkey("root")
    print(f"Root will yell {result}")
