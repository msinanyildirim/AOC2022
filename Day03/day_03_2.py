import string

def itemToPriority(item):
   return string.ascii_letters.index(item) + 1

with open("./input_03.txt", 'r') as file:
    backpack_contents = file.read().splitlines()

group_size = 3
assert len(backpack_contents) % group_size == 0, f"There are {len(backpack_contents)} elves which is not a multiple of {group_size}."

backpack_contents = [set(content) for content in backpack_contents]

badges = []
for curr_ind in range(0, len(backpack_contents), group_size):
    group_backpack_contents = backpack_contents[curr_ind:curr_ind + group_size]

    common_set = set.intersection(*group_backpack_contents)
    assert len(common_set) == 1, f"{group_backpack_contents} has more than one common item"

    badges.append(common_set.pop())

final_sum = sum(itemToPriority(item) for item in badges)

print(f"Final sum of priorities of badges is {final_sum}.")
