import pdb
import re
from itertools import takewhile

from input import INPUT

PLANE_ROWS = 128
PLANE_COLUMNS = 8


def recursive_solve_row_code(row_code, rows_minimum, rows_maximum):
    if len(row_code) == 1:
        # print(f"MIN:    {rows_minimum}")
        # print(f"MAX:    {rows_maximum}")
        if row_code == "F":
            return rows_minimum
        else:
            return rows_maximum - 1
    else:
        row_code_decision = row_code[0]
        remaining_row_code = row_code[1:]

        # print(f"CUR: {row_code_decision}")
        # print(f"LEFT:   {remaining_row_code}")
        # print(f"MIN:    {rows_minimum}")
        # print(f"MAX:    {rows_maximum}")
        # print("==========")

        if row_code_decision == "F":
            return recursive_solve_row_code(remaining_row_code, rows_minimum, rows_maximum - (((rows_maximum - rows_minimum) / 2)))
        else:
            return recursive_solve_row_code(remaining_row_code, rows_minimum + (((rows_maximum - rows_minimum) / 2)), rows_maximum)


def calculate_all_possible_seats():
    possible_seat_ids = []

    for row in range(PLANE_ROWS-1):
        for col in range(PLANE_COLUMNS-1):
            possible_seat_ids.append((row * 8) + col)

    return possible_seat_ids


def recursive_solve_column_code(column_code, col_minimum, col_maximum):
    if len(column_code) == 1:
        if column_code == "R":
            return col_maximum - 1
        else:
            return col_minimum
    else:
        col_decision_code = column_code[0]
        remaining_col_code = column_code[1:]

        if col_decision_code == "L":
            return recursive_solve_column_code(remaining_col_code, col_minimum, col_maximum - (((col_maximum - col_minimum) / 2)))
        else:
            return recursive_solve_column_code(remaining_col_code, col_minimum + (((col_maximum - col_minimum) / 2)), col_maximum)


def solve_part_one():
    seat_ids = []
    seating_codes = [seating_code for seating_code in INPUT.split()]

    for seating_code in seating_codes:
        row_code = seating_code[:7]
        column_code = seating_code[7:]

        row_number = recursive_solve_row_code(row_code, 0, PLANE_ROWS)
        col_number = recursive_solve_column_code(column_code, 0, PLANE_COLUMNS)

        seat_ids.append((row_number * 8) + col_number)

    seat_ids.sort()
    # print(f"Highest Seat Id:    {seat_ids[-1]}")
    return seat_ids



def solve_part_two():
    seat_ids = solve_part_one()
    possible_seats = []

    for seat in seat_ids:
        if (seat + 2) in seat_ids and (seat + 1) not in seat_ids:
            possible_seats.append(seat)
        if (seat - 2) in seat_ids and (seat - 1) not in seat_ids:
            possible_seats.append(seat)

    possible_seats = set(possible_seats)

    print(f"Possible Seats: {possible_seats}")

    # all_seat_ids = calculate_all_possible_seats()
    # empty_seats = []
    # potential_seat_ids = []

    # print(f"{len(seat_ids)}     {len(all_seat_ids)}")

    # for seat in all_seat_ids:
    #     if seat not in seat_ids:
    #         empty_seats.append(seat)

    # for seat in empty_seats:
    #     if (seat + 1) in seat_ids:
    #         potential_seat_ids.append(seat)
    #     if (seat - 1) in seat_ids:
    #         potential_seat_ids.append(seat)

    # valid_potential_seat_ids = set(potential_seat_ids)

    # print(f"Potential Seats: {valid_potential_seat_ids}")


def main():
    # solve_part_one()
    solve_part_two()



if __name__ == '__main__':
    main()