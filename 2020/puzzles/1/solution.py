from puzzle_input import PUZZLE_INPUT


def solve_part_one():
    print('Solving')

    valid_count = 0
    invalid_count = 0

    for record in PUZZLE_INPUT:
        minimum = int(record[0])
        maximum = int(record[1])
        letter = record[2]
        password = record[3]

        count = int(password.count(letter))

        if minimum <= count and count <= maximum:
            valid_count += 1
        else:
            invalid_count += 1

    print(f"Valid:   {valid_count}")
    print(f"Invalid:   {invalid_count}")


def solve_part_two():
    valid_count = 0
    invalid_count = 0

    for record in PUZZLE_INPUT:
        try:
            password = record[3]
            letter = record[2]

            character_one = password[int(record[0]) - 1]
            character_two = password[int(record[1]) - 1]

            if character_one != letter and character_two != letter:
                invalid_count += 1
                continue

            if character_one == letter and character_two == letter:
                invalid_count += 1
                continue

            if character_one == letter and character_two != letter:
                valid_count += 1
                continue
            
            if character_two == letter and character_one != letter:
                valid_count += 1
                continue

            count = int(password.count(letter))

            if minimum <= count and count <= maximum:
                valid_count += 1
            else:
                invalid_count += 1
        except IndexError as e:
            print(record)

    print(f"Valid:   {valid_count}")
    print(f"Invalid:   {invalid_count}")


def main():
    # solve_part_one()
    solve_part_two()



if __name__ == '__main__':
    main()
