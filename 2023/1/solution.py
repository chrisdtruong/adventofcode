from input import input_data




def solve_part_one():
    sum = 0

    for line in input_data:
        number = ""
        # get first digit
        for character in line:
            if character.isdigit():
                number += character
                break
        # get last digit
        for character in line[::-1]:
            if character.isdigit():
                number += character
                break

        sum += int(number)

    print(f"Answer:  {sum}")

NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def solve_part_two():
    sum = 0

    for line in input_data:
        number = ""
        real_number = ""

        # get first digit
        for character in line:
            real_number += character
            numbers_found = [num for num in NUMBERS.keys() if num in real_number]
            if len(numbers_found) > 0:
                number += str(NUMBERS[numbers_found[0]])
                real_number = ""
                break

            if character.isdigit():
                number += character
                real_number = ""
                break

        # get last digit
        for character in line[::-1]:
            real_number += character

            numbers_found = [num for num in NUMBERS.keys() if num in real_number[::-1]]
            if len(numbers_found) > 0:
                number += str(NUMBERS[numbers_found[0]])
                real_number = ""
                break

            if character.isdigit():
                number += character
                real_number = ""
                break

        sum += int(number)

    print(f"Answer:  {sum}")

def main():
    solve_part_one()
    solve_part_two()

if __name__ == "__main__":
    main()