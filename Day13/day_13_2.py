
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

    packet_list = puzzle_input.split("\n")
    packet_list = [eval(packet) for packet in packet_list if packet != '']

    separator_packet_one = [[2]]
    separator_packet_two = [[6]]

    packet_list.append(separator_packet_one)
    packet_list.append(separator_packet_two)

    sorted_packets = []
    for packet in packet_list:
        for i, elem in enumerate(sorted_packets):
            if compare_packets(packet, elem) == 1:
                sorted_packets.insert(i, packet)
                break
        else:
            sorted_packets.append(packet)

    separator_one_index = sorted_packets.index(separator_packet_one) + 1
    separator_two_index = sorted_packets.index(separator_packet_two) + 1

    print(separator_one_index * separator_two_index)
