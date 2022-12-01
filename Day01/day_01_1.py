with open('input_01.txt', 'r') as file:
    vals = file.readlines()

currmax = 0
currsum = 0
for elem in vals:
    if elem != "\n":
        currcal = int(elem)
        currsum += currcal
    elif elem == "\n":
        if currsum > currmax:
            currmax = currsum
        currsum = 0
else:
    if currsum > currmax:
        currmax = currsum
    currsum = 0

print(f"The final answer is {currmax}")
