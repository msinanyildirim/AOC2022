import string

def itemToPriority(item):
   return string.ascii_letters.index(item) + 1

with open("./input_03.txt", 'r') as file:
    backpack_contents = file.read().splitlines()

misplaced_items = []

for backpack_content in backpack_contents:
    assert len(backpack_content) % 2 == 0, f"{backpack_content} has an odd number of items."

    half_point = len(backpack_content) // 2
    first_half, second_half = backpack_content[:half_point], backpack_content[half_point:]

    common_set = set(first_half) & set(second_half)
    assert len(common_set) == 1, f"{backpack_content} has more than one common item"

    misplaced_items.append(common_set.pop())

final_sum = sum(itemToPriority(item) for item in misplaced_items)

print(f"Final sum of priorities of misplaced items is {final_sum}.")
