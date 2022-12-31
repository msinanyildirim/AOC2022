class LinkElement:
    def __init__(self, value, next_elem=None, prev_elem=None):
        self.value = value
        self.prev = prev_elem
        self.next = next_elem


class LinkedList:
    def __init__(self, input_list: list):
        self.list = []
        for value in input_list:
            curr_elem = LinkElement(value)
            self.list.append(curr_elem)

        # Linking the elements in both directions
        self.list[0].next = self.list[1]
        self.list[0].prev = self.list[-1]

        for temp_idx in range(1, len(self.list) - 1):
            curr_elem = self.list[temp_idx]
            curr_elem.prev = self.list[temp_idx - 1]
            curr_elem.next = self.list[temp_idx + 1]

        self.list[-1].next = self.list[0]
        self.list[-1].prev = self.list[-2]

    def decrypt(self, decryption_key):
        for curr_elem in self.list:
            curr_elem.value *= decryption_key

        for _ in range(10):
            self.mixing()

    def mixing(self):
        for curr_linked_elem in self.list:
            # print(self) # This prints the list to check for the test case
            curr_value = curr_linked_elem.value

            # Reducing the number since one cycle of rotation would result in the same state
            if curr_value > 0:
                curr_value = curr_value % (len(self.list) - 1)
            elif curr_value < 0:
                curr_value = curr_value % (len(self.list) - 1) - (len(self.list) - 1)

            if curr_value > 0:
                # Remove current element from the list
                curr_linked_elem.prev.next = curr_linked_elem.next
                curr_linked_elem.next.prev = curr_linked_elem.prev

                # Go curr_value times in the positive direction
                shift_elem = curr_linked_elem
                for _ in range(abs(curr_value)):
                    shift_elem = shift_elem.next

                # Insert current element according to shift_elem
                curr_linked_elem.prev = shift_elem
                curr_linked_elem.next = shift_elem.next
                shift_elem.next.prev = curr_linked_elem
                shift_elem.next = curr_linked_elem
            elif curr_value < 0:
                # Remove current element from the list
                curr_linked_elem.prev.next = curr_linked_elem.next
                curr_linked_elem.next.prev = curr_linked_elem.prev

                # Go curr_value times in the negative direction
                shift_elem = curr_linked_elem
                for _ in range(abs(curr_value)):
                    shift_elem = shift_elem.prev

                # Insert current element according to shift_elem
                curr_linked_elem.next = shift_elem
                curr_linked_elem.prev = shift_elem.prev
                shift_elem.prev.next = curr_linked_elem
                shift_elem.prev = curr_linked_elem

    def find_elem_with_value(self, value):
        for elem in self.list:
            if elem.value == value:
                return elem
        else:
            raise Exception(f"No element with {value=} found.")

    def get_coordinates(self):
        start_elem = self.find_elem_with_value(0)

        result = []
        curr_elem = start_elem
        for _ in range(3):
            for _ in range(1000):
                curr_elem = curr_elem.next
            result.append(curr_elem.value)

        return result

    def __repr__(self):
        result = []

        curr_elem = self.list[0]
        for _ in range(len(self.list)):
            result.append(curr_elem.value)
            curr_elem = curr_elem.next

        return str(result)


if __name__ == "__main__":
    with open("input_20.txt", "r") as file:
        puzzle_input = file.read().splitlines()

    input_list = [int(line) for line in puzzle_input]

    linked_list = LinkedList(input_list)

    decryption_key = 811589153
    linked_list.decrypt(decryption_key)

    print(f"Sum of the coordinates is {sum(linked_list.get_coordinates())}")
