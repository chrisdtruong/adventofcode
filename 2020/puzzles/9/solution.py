import pdb
import re
from itertools import takewhile

from input import INPUT, SAMPLE

USE_SAMPLE = True
PREAMBLE_LENGTH = 5

def get_numbers() -> list:
    if USE_SAMPLE:
        return [int(value) for value in SAMPLE.split('\n')]
    else:
        return [int(value) for value in INPUT.split('\n')]


def solve_part_one() -> int:
    numbers = get_numbers()
    print(numbers)
    return 0


def solve_part_two() -> int:
    return 0


def main() -> None:
    print(f"Part One:   {solve_part_one()}")
    print(f"Part Two:   {solve_part_two()}")


if __name__ == '__main__':
    main()