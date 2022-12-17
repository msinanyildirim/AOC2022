import re

def manhattan_dist(point1, point2):
    distx = abs(point1[0] - point2[0])
    disty = abs(point1[1] - point2[1])
    return distx + disty


def read_puzzle_input(input_file_path):

    with open(input_file_path, "r") as file:
        puzzle_input = file.read().splitlines()

    sensors_pos = []
    beacons_pos = []

    for puzzle_line in puzzle_input:
        xvals = re.findall("x=([\-\d]+)", puzzle_line)
        yvals = re.findall("y=([\-\d]+)", puzzle_line)

        curr_sensor_pos = [int(xvals[0]), int(yvals[0])]
        curr_beacon_pos = [int(xvals[1]), int(yvals[1])]
        
        sensors_pos.append(curr_sensor_pos)
        beacons_pos.append(curr_beacon_pos)

    return sensors_pos, beacons_pos


def impossible_ranges(sensors_pos, beacons_pos, curry):

    no_beacon_intervals = []
    for curr_sensor, curr_beacon in zip(sensors_pos, beacons_pos):
        curr_dist = manhattan_dist(curr_sensor, curr_beacon)

        curr_sensorx, curr_sensory = curr_sensor

        curry_dist = abs(curr_sensory - curry)
        currx_dist = curr_dist - curry_dist

        if currx_dist < 0 :
            continue
        else:
            curr_stat = [curr_sensorx - currx_dist, curr_sensorx + currx_dist]
            no_beacon_intervals.append(curr_stat)

    no_beacon_intervals = sorted(no_beacon_intervals)

    return no_beacon_intervals


def merge_intervals(sorted_intervals):

    merged_intervals = []

    curr_interval = sorted_intervals[0]
    for next_interval in sorted_intervals[1:]:

        if next_interval[0] > curr_interval[1]: 
            # current interval and next interval do not coincide
            merged_intervals.append(curr_interval)
            curr_interval = next_interval
            continue
        else:
            # Merge the intervals
            curr_interval[1] = max(curr_interval[1], next_interval[1])
            continue
    else:
        merged_intervals.append(curr_interval)

    return merged_intervals


def unique_elems(input_list):
    unique_elems_list = []
    for curr_elem in input_list:
        if curr_elem in unique_elems_list:
            continue
        else:
            unique_elems_list.append(curr_elem)

    return unique_elems_list


def get_beacons_x_in_row(beacons_pos, curry):

    unique_beacons = unique_elems(beacons_pos)

    curr_row_beacons_x = []
    for curr_beacon in unique_beacons:
        if curr_beacon[1] == curry:
            curr_row_beacons_x.append(curr_beacon[0])

    curr_row_beacons_x.sort()
    return curr_row_beacons_x


def num_beacons_in_interval(interval, beacon_x):

    interval_start, interval_end = interval
    
    num_beacons = 0
    for curr_x in beacon_x:
        if curr_x >= interval_start and curr_x <= interval_end:
            num_beacons += 1

    return num_beacons


def no_beacons_in_row(merged_intervals, beacons_pos, curry):

    beacon_x = get_beacons_x_in_row(beacons_pos, curry)

    num_no_beacon_locations = 0
    for curr_interval in merged_intervals:
        curr_width = curr_interval[1] - curr_interval[0] + 1

        num_beacons_in_curr_interval = num_beacons_in_interval(curr_interval, beacon_x)

        num_no_beacon_locations += curr_width - num_beacons_in_curr_interval
    
    return num_no_beacon_locations


if __name__ == "__main__":
    sensors_pos, beacons_pos = read_puzzle_input("./input_15.txt")
    curr_y = 2_000_000
    no_beacon_intervals = impossible_ranges(sensors_pos, beacons_pos, curr_y)
    merged_intervals = merge_intervals(no_beacon_intervals)
    result = no_beacons_in_row(merged_intervals, beacons_pos, curr_y)
    print(result)

