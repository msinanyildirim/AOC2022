with open("./input_06.txt", "r") as file:
    datastream = file.read()

unique_length = 4
for curr_index in range(unique_length ,len(datastream)):
    curr_buffer = datastream[curr_index-unique_length :curr_index]
    if len(curr_buffer) == len(set(curr_buffer)):
        break

final_result = curr_index
print(f"Message starts after character number {final_result}")

