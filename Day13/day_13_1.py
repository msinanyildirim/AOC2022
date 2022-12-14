
def compare_packets(packet_one, packet_two):
    if type(packet_one) == int and type(packet_two) == int:
        if packet_one < packet_two :
            return 1
        elif packet_one > packet_two:
            return -1
        else:
            return 0

    elif type(packet_one) == list and type(packet_two) == int:
        return compare_packets(packet_one, [packet_two])

    elif type(packet_one) == int and type(packet_two) == list:
        return compare_packets([packet_one], packet_two)

    elif type(packet_one) == list and type(packet_two) == list:
        for packet_one_elem, packet_two_elem in zip(packet_one, packet_two):
            curr_result = compare_packets(packet_one_elem, packet_two_elem)
            if curr_result == 0:
                continue
            else:
                return curr_result
        else:
            packet_one_len = len(packet_one)
            packet_two_len = len(packet_two)
            return compare_packets(packet_one_len, packet_two_len)
    else:
        raise Exception(f"The packets have types {type(packet_one)} and {type(packet_two)}")




if __name__ == "__main__":

    with open("./input_13.txt", "r") as file:
        puzzle_input = file.read()

    pairs_string = puzzle_input.split("\n\n")
    pairs_string = [pair.split("\n") for pair in pairs_string]

    right_order_ind = []
    for i, curr_pair in enumerate(pairs_string, start=1):
        packet_one = eval(curr_pair[0])
        packet_two = eval(curr_pair[1])

        curr_result = compare_packets(packet_one, packet_two)
        if curr_result == 1:
            right_order_ind.append(i)

    print(sum(right_order_ind))
