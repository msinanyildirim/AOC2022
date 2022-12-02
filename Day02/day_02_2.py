with open("input_02.txt", 'r') as file:
    plays = file.readlines()

shape_score = {"R": 1, "P":2, "S":3}
strat = {"A X": "S", "A Y": "R", "A Z": "P", "B X": "R", "B Y": "P", "B Z": "S", "C X": "P", "C Y": "S", "C Z": "R"}
result_score = {"X": 0, "Y": 3, "Z":6 }

curr_score = 0
for curr_round in plays:
    curr_score += shape_score[strat[curr_round[:3]]] + result_score[curr_round[2]]

print(f"Final score is {curr_score}")
