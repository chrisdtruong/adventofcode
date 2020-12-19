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


def execute_instructions(instructions: list) -> [int, str]:
    accumulator = 0
    current_instruction = 0
    instruction_manual = set()
    end_of_instructions = False
    is_infinite_loop = True

    while not end_of_instructions:
        try:
            instruction = instructions[current_instruction]

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
                end_of_instructions = True
        except IndexError as e:
            end_of_instructions = True
            is_infinite_loop = False

    return accumulator, is_infinite_loop


def solve_part_one() -> int:
    list_of_instructions = get_list_of_instructions()

    accumulator, is_infinite = execute_instructions(list_of_instructions)

    return accumulator


def solve_part_two() -> int:
    list_of_instructions = get_list_of_instructions()

    # Switch jmp => nop
    indexes_with_jmp = [index for index in range(len(list_of_instructions)) if 'jmp' in list_of_instructions[index]]

    for index in indexes_with_jmp:
        # Deep Copy
        copy_of_instructions = [i for i in list_of_instructions]
        copy_of_instructions[index] = copy_of_instructions[index].replace('jmp', 'nop')

        accumulator, is_infinite = execute_instructions(copy_of_instructions)

        if is_infinite is False:
            return accumulator

    # Switch nop => jmp
    indexes_with_jmp = [index for index in range(len(list_of_instructions)) if 'nop' in list_of_instructions[index]]

    for index in indexes_with_jmp:
        # Deep Copy
        copy_of_instructions = [i for i in list_of_instructions]
        copy_of_instructions[index] = copy_of_instructions[index].replace('nop', 'jmp')

        accumulator, is_infinite = execute_instructions(copy_of_instructions)

        if is_infinite is False:
            return accumulator

    return 0


def main() -> None:
    print(f"Part One:   {solve_part_one()}")
    print(f"Part Two:   {solve_part_two()}")


if __name__ == '__main__':
    main()