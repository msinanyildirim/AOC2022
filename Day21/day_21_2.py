def solve_monkey(monkey_name):

    if is_human_dependent(monkey_name):
        raise Exception(f"Monkey {monkey_name} depends on humn, its result cannot be calculated")

    curr_operation = monkeys[monkey_name]

    if len(curr_operation) == 1:
        return int(curr_operation[0])
    elif len(curr_operation) == 3:
        monkey1_name = curr_operation[0]
        monkey2_name = curr_operation[2]

        monkey1 = solve_monkey(monkey1_name)
        math_operation = curr_operation[1]
        monkey2 = solve_monkey(monkey2_name)

        monkey_result = eval(f"{monkey1} {math_operation} {monkey2}")
        monkeys[monkey_name] = monkey_result
        return monkey_result
    else:
        raise Exception(f"{monkey_name} has an operation with unexpected length")


def is_human_dependent(monkey_name):
    curr_operation = monkeys[monkey_name]

    if len(curr_operation) == 1:
        if monkey_name == "humn":
            return True
        else:
            return False
    elif len(curr_operation) == 3:
        monkey1_name = curr_operation[0]
        monkey2_name = curr_operation[2]

        monkey1 = is_human_dependent(monkey1_name)
        monkey2 = is_human_dependent(monkey2_name)

        monkey_dependence = monkey1 or monkey2

        return monkey_dependence
    else:
        raise Exception(f"{monkey_name} has unexpected length")


def reverse_operation(wanted_result, operand1, operand2, operation):
    if operand1 == "unk" and operand2 != "unk":
        if operation == "+":
            return wanted_result - operand2
        elif operation == "-":
            return wanted_result + operand2
        elif operation == "*":
            return wanted_result / operand2
        elif operation == "/":
            return wanted_result * operand2
        else:
            raise Exception(f"Unexpected operation {operation}")

    elif operand2 == "unk" and operand1 != "unk":
        if operation == "+":
            return wanted_result - operand1
        elif operation == "-":
            return operand1 - wanted_result
        elif operation == "*":
            return wanted_result / operand1
        elif operation == "/":
            return operand1 / wanted_result
        else:
            raise Exception(f"Unexpected operation {operation}")

    else:
        raise Exception(f"One of the operands should be 'unk' but here we have {operand1=} and {operand2=}")


def should_equal(orig_monkey, wanted_value):
    orig_operation = monkeys[orig_monkey]
    next_monkey1 = orig_operation[0]
    next_monkey2 = orig_operation[2]
    math_operation = orig_operation[1]

    if (is_human_dependent(next_monkey1)) and (not is_human_dependent(next_monkey2)):
        new_value = reverse_operation(wanted_value, "unk", solve_monkey(next_monkey2), math_operation)
        if next_monkey1 == "humn":
            return new_value
        else:
            return should_equal(next_monkey1, new_value)

    elif (is_human_dependent(next_monkey2)) and (not is_human_dependent(next_monkey1)):
        new_value = reverse_operation(wanted_value, solve_monkey(next_monkey1), "unk", math_operation)
        if next_monkey2 == "humn":
            return new_value
        else:
            return should_equal(next_monkey2, new_value)

    else:
        raise Exception(f"This exception should not be raised. Operation is {next_monkey1} {math_operation} "
                        f"{next_monkey2} and we have {is_human_dependent(next_monkey1)=} "
                        f"and {is_human_dependent(next_monkey2)=}")


if __name__ == "__main__":
    with open("input_21.txt", "r") as file:
        puzzle_input = file.read().splitlines()

    monkeys = [curr_line.split() for curr_line in puzzle_input]
    monkeys = {monkey[0][:-1]: monkey[1:] for monkey in monkeys}

    root_operation = monkeys["root"]
    root_monkey1 = root_operation[0]
    root_monkey2 = root_operation[2]

    if (is_human_dependent(root_monkey1)) and (not is_human_dependent(root_monkey2)):
        monkey2_result = solve_monkey(root_monkey2)
        result = should_equal(root_monkey1, monkey2_result)
    elif (is_human_dependent(root_monkey2)) and (not is_human_dependent(root_monkey1)):
        monkey1_result = solve_monkey(root_monkey1)
        result = should_equal(root_monkey2, monkey1_result)
    else:
        raise Exception("This exception should not be reached.")

    print(f"humn should yell {result}")
