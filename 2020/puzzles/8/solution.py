import pdb
import re
from itertools import takewhile

from input import INPUT


def get_list_of_instructions() -> list:
    return INPUT.split('\n')


def process_instruction(instruction: str) -> list:
    operation, argument = instruction.split(" ")
    sign = argument[:1]
    amount = argument[1:]

    return operation, sign, int(amount)


def solve_part_one() -> int:
    list_of_instructions = get_list_of_instructions()

    accumulator = 0
    current_instruction = 0
    instruction_manual = set()
    end_of_infinite_loop = False

    while not end_of_infinite_loop:
        instruction = list_of_instructions[current_instruction]

        if current_instruction not in instruction_manual:
            # Do Command
            operation, sign, amount = process_instruction(instruction)
            instruction_manual.add(current_instruction)

            if operation == 'acc':
                if sign == '+':
                    accumulator += amount
                else:
                    accumulator -= amount
                current_instruction += 1
            elif operation == 'jmp':
                if sign == '+':
                    current_instruction += amount
                else:
                    current_instruction -= amount
            elif operation == 'nop':
                current_instruction += 1
            else:
                raise Exception("uhhh ohhh")

        else:
            # We Are Done
            end_of_infinite_loop = True

    return accumulator


def solve_part_two() -> int:
    return 0


def main() -> None:
    print(f"Part One:   {solve_part_one()}")
    print(f"Part Two:   {solve_part_two()}")


if __name__ == '__main__':
    main()