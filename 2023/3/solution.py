from input import INPUT_DATA

DEBUG = False

def store_index(row, column):
    return f"{row}-{column}"


def read_index(index):
    return index.split("-")


def load_part_map(input_data):
    part_map = []
    for line in input_data.splitlines():
        part_map.append([char for char in line])

    return(part_map)


def build_part_number_map_index(part_map):
    parts = []
    gears = []
    number_index = {}

    for row, part_row in enumerate(part_map):
        current_number = ""
        current_number_indexes = []

        for column, character in enumerate(part_row):
            if character == ".":
                if current_number != "":
                    # number is complete
                    real_number = int(current_number)
                    for index in current_number_indexes:
                        number_index[index] = {
                            "number": real_number,
                            "indexes": current_number_indexes
                        }

                    current_number = ""
                    current_number_indexes = []

                # not part or number
                continue
            elif character.isdigit():
                current_number += character
                current_number_indexes.append(store_index(row, column))
            else:
                if character == "*":
                    gears.append([row, column])

                # it is a part
                parts.append([row, column])

                if current_number != "":
                    # number is complete
                    real_number = int(current_number)
                    for index in current_number_indexes:
                        number_index[index] = {
                            "number": real_number,
                            "indexes": current_number_indexes
                        }

                    current_number = ""
                    current_number_indexes = []

        # End of Line, check if number exists
        if current_number != "":
            # number is complete
            real_number = int(current_number)
            for index in current_number_indexes:
                number_index[index] = {
                    "number": real_number,
                    "indexes": current_number_indexes
                }

            current_number = ""
            current_number_indexes = []

    if DEBUG:
        print(f"Parts:  {parts}")
        print(f"Number Index:   {number_index}")

    return [parts, number_index, gears]

def get_adjacent_number_for_part(part, number_index, observed_indexes, part_map):
    part_row, part_column = part
    # get number for each coordinate around the part
    numbers = []

    check_points = [
        [-1, -1],   # top left
        [-1, 0],    # left
        [-1, 1],    # bottom left
        [0, -1],    # top
        [0, 1],     # bottom
        [1, -1],     # top right
        [1, 0],      # right
        [1, 1]      # bottom right
    ]
    for check_point in check_points:
        row_offset, column_offset = check_point
        checkpoint_index = store_index(part_row + row_offset, part_column + column_offset)
        if DEBUG:
            print(f"[{checkpoint_index}] - {part_map[part_row + row_offset][part_column + column_offset]}")
        if checkpoint_index in number_index:
            
            numbers.append(number_index[checkpoint_index])

    if DEBUG:
        print(numbers)
    # remove duplicate_numbers
    unique_numbers = []
    for number in numbers:
        if number["indexes"][0] not in observed_indexes:
            unique_numbers.append(number["number"])
            observed_indexes += number["indexes"]

    return unique_numbers

def solve_part_one():
    part_total = 0
    observed_number_indexes = []

    part_map = load_part_map(INPUT_DATA)
    parts, number_index, _ = build_part_number_map_index(part_map)

    # DBEUG - get_adjacent_number_for_part([2,136], number_index, observed_number_indexes, part_map)
    for part in parts:
        numbers = get_adjacent_number_for_part(part, number_index, observed_number_indexes, part_map)
        if DEBUG:
            print(f"Part:    {part} - Numbers:    {numbers}")
        for number in numbers:
            part_total += number

    print(f"Answer:  {part_total}")


def solve_part_two():
    gear_ratio_total = 0
    observed_number_indexes = []

    part_map = load_part_map(INPUT_DATA)
    _, number_index, gears = build_part_number_map_index(part_map)
    
    for gear in gears:
        numbers = get_adjacent_number_for_part(gear, number_index, observed_number_indexes, part_map)
        if len(numbers) != 2:
            continue

        gear_ratio = numbers[0] * numbers[1]
        gear_ratio_total += gear_ratio

    print(f"Answer:  {gear_ratio_total}")

def main():
    solve_part_one()
    solve_part_two()


if __name__ == "__main__":
    main()