with open("./input_04.txt", 'r') as file:
    complete_assignments = file.read().splitlines()

num_fully_contained = 0
for curr_assignment in complete_assignments:
    first_elf_assignment, second_elf_assignment = curr_assignment.split(",")
    
    first_elf_assignment = first_elf_assignment.split("-")
    second_elf_assignment = second_elf_assignment.split("-")

    first_elf_assignment = [int(elem) for elem in first_elf_assignment]
    second_elf_assignment = [int(elem) for elem in second_elf_assignment]

    if (first_elf_assignment[0] - second_elf_assignment[0])*(first_elf_assignment[1]-second_elf_assignment[1]) <= 0:
        num_fully_contained += 1

print(f"Number of elves whose assignments is fully contained in the assignment of their partner is {num_fully_contained}")
