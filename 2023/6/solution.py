from .input import INPUT_DATA


def solve_part_one():
    """
    H = milliseconds button held
    S = speed of the boat (millimeter/ millisecond)
    D = distance of the boat (millimeters)
    T = time of race in milliseconds

    D  =  (T - H) * H
    10  =  (7 - 5) * (5 * 1)

    Figure out the range of H, that D is greater then then X, X being the goal to beat

    Example: Time of 15, Distance of 40

    40 = (15 - H) * H
    40 = (15 * H) - (H * H)
    0 = 15H - H^2 - 40
    """
    return 0


def solve_part_two():
    return 0


def main():
    print(f"Answer 1:     {solve_part_one()}")
    print(f"Answer 2:     {solve_part_two()}")


if __name__ == "__main__":
    main()