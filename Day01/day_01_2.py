with open('input_01.txt', 'r') as file:
    vals = file.readlines()

currmax = [0, 0, 0]
currsum = 0
for elem in vals:
    if elem != "\n":
        currcal = int(elem)
        currsum += currcal
    elif elem == "\n":
        if currsum > currmax[-1]:
            currmax[-1] = currsum
            currmax.sort(reverse=True)
        currsum = 0
else:
    if currsum > currmax[-1]:
        currmax[-1] = currsum
        currmax.sort(reverse=True)
    currsum = 0

print(f"The final answer is {sum(currmax)}")
