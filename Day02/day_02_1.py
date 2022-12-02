with open("input_02.txt", 'r') as file:
    plays = file.readlines()

shape_score = {"X": 1, "Y":2, "Z":3}
result_score = {"A X":3, "A Y":6, "A Z":0, "B X":0, "B Y":3, "B Z":6, "C X":6, "C Y":0, "C Z":3}

curr_score = 0
for curr_round in plays:
    curr_score += shape_score[curr_round[2]] + result_score[curr_round[:3]]

print(f"Final score is {curr_score}")
