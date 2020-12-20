import pdb
import re
from itertools import takewhile

from input import INPUT, SAMPLE

USE_SAMPLE = False
PREAMBLE_LENGTH = 25


def get_numbers() -> list:
    if USE_SAMPLE:
        return [int(value) for value in SAMPLE.split('\n')]
    else:
        return [int(value) for value in INPUT.split('\n')]


def current_number_valid_for_preamble(number: int, preamble: list) -> bool:
    found_match = False
    
    for num_one in preamble:
        for num_two in preamble:
            if (num_one + num_two) == number:
                return True

    return False


def get_contiguous_set_of_numbers(target_number: int, number_list: list) -> list:
    for bottom_window in range(len(number_list)):
        base_number = number_list[bottom_window]
        total = 0

        for top_window in range(bottom_window+1, len(number_list)):
            total += number_list[top_window]

            if total == target_number and (top_window - bottom_window) > 1:
                return number_list[bottom_window+1:top_window]
            elif total > target_number:
                break
            else:
                pass


def solve_part_one() -> int:
    numbers = get_numbers()
    
    window_min = 0
    window_max = PREAMBLE_LENGTH
    preamble = numbers[window_min:window_max]

    # Start at the end of the Preamble
    index = PREAMBLE_LENGTH

    while index < len(numbers):

        current_number = numbers[index]

        if current_number_valid_for_preamble(current_number, preamble) is True:
            index += 1
            window_min += 1
            window_max += 1
            preamble = numbers[window_min:window_max]
        else:
            return current_number

    return 0


def solve_part_two() -> int:
    number_list = get_numbers()
    target_number = solve_part_one()

    contiguous_numbers = get_contiguous_set_of_numbers(target_number, number_list)
    
    contiguous_numbers.sort()

    answer = contiguous_numbers[0] + contiguous_numbers[-1]

    return answer


def main() -> None:
    print(f"Part One:   {solve_part_one()}")
    print(f"Part Two:   {solve_part_two()}")


if __name__ == '__main__':
    main()