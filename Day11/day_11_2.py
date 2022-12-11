import re

def monkey_oper_decor(input_str):
    return lambda old: eval(input_str.replace("old", str(old)))

def monkey_test_decor(input_divisor, input_true_dest, input_false_dest):
    return lambda worry: input_true_dest if worry % input_divisor == 0 else input_false_dest

def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)

def lcm(a, b):
    return (a / gcd(a, b)) * b

with open("./input_11.txt", "r") as file:
    puzzle_input = file.read()

monkey_string_list = [temp.splitlines() for temp in puzzle_input.split("\n\n")]

monkey_states = {}
test_lcm = 1
for curr_monkey_string in monkey_string_list:
    monkey_ind = re.search("Monkey (\d+):", curr_monkey_string[0]).group(1)
    monkey_states[monkey_ind] = {}

    items_worry_list = curr_monkey_string[1][18:].split(", ")
    items_worry = [int(item_worry) for item_worry in items_worry_list]
    monkey_states[monkey_ind]["items_worry"] = items_worry

    monkey_operation = monkey_oper_decor(curr_monkey_string[2][19:])
    monkey_states[monkey_ind]["monkey_oper"] = monkey_operation

    monkey_divisor = int(curr_monkey_string[3][-2:])
    monkey_true_dest = curr_monkey_string[4][29:]
    monkey_false_dest = curr_monkey_string[5][30:]
    
    monkey_states[monkey_ind]["monkey_test"] = monkey_test_decor(monkey_divisor, monkey_true_dest, monkey_false_dest)

    monkey_states[monkey_ind]["inspected_times"] = 0
    
    test_lcm = lcm(test_lcm, monkey_divisor)

N = 10000
num_monkeys = len(monkey_states)
for _ in range(N):
    for monkey_ind in range(num_monkeys):
        curr_monkey = monkey_states[str(monkey_ind)]
        for worry_level in curr_monkey["items_worry"]:
            after_worry = curr_monkey["monkey_oper"](worry_level)
            after_worry = after_worry % test_lcm # Because getting the number mod lcm would not change the divisibility test results
            throw_to_ind = curr_monkey["monkey_test"](after_worry)
            monkey_states[throw_to_ind]["items_worry"].append(after_worry)
            curr_monkey["inspected_times"] += 1
        
        curr_monkey["items_worry"] = []

final_numbers = sorted([monkey["inspected_times"] for monkey_ind, monkey in monkey_states.items()], reverse=True)
final_result = final_numbers[0]*final_numbers[1]
print(f"Final monkey business is {final_result}")

