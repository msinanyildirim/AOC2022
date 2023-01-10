def snafu_to_dec(quin_num: str):
    sym_to_num = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
    result_dec = 0
    for i, d in enumerate(quin_num[::-1]):
        result_dec += sym_to_num[d] * (5**i)

    return result_dec


def dec_to_snafu(dec_num: int):
    num_to_sym = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}
    snafu_num = ""
    while dec_num != 0:
        curr_digit = dec_num % 5
        if curr_digit > 2:
            curr_digit -= 5
        snafu_num = num_to_sym[curr_digit] + snafu_num
        dec_num -= curr_digit
        dec_num = dec_num // 5

    return snafu_num


if __name__ == "__main__":
    with open("input_25.txt", "r") as file:
        puzzle_input = file.read().splitlines()

    fuel_amounts_snafu = puzzle_input
    fuel_amounts_dec = [snafu_to_dec(curr_snafu) for curr_snafu in fuel_amounts_snafu]

    total_fuel_dec = sum(fuel_amounts_dec)
    total_fuel_snafu = dec_to_snafu(total_fuel_dec)

    print(f"Total fuel amount as a snafu number is {total_fuel_snafu}")
