with open("./input_04.txt", 'r') as file:
    complete_assignments = file.read().splitlines()

num_overlapped_pairs = 0
for curr_assignment in complete_assignments:
    first_elf_assignment, second_elf_assignment = curr_assignment.split(",")
    
    first_elf_assignment = first_elf_assignment.split("-")
    second_elf_assignment = second_elf_assignment.split("-")

    first_elf_assignment = [int(elem) for elem in first_elf_assignment]
    second_elf_assignment = [int(elem) for elem in second_elf_assignment]

    if (second_elf_assignment[1] - first_elf_assignment[0])*(second_elf_assignment[0]-first_elf_assignment[1]) <= 0:
        num_overlapped_pairs += 1

print(f"Number of paris of elves whose assignments overlap is {num_overlapped_pairs}")
