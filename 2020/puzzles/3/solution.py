import pdb
from functools import reduce

from input import INPUT


def solve_part_one(across=3, down=1):

    elevation = 0
    longitude = 0

    trees_encountered = 0
    open_spaces = 0

    width_of_mountain = len(INPUT.splitlines()[1])
    bottom_of_mountain = len(INPUT.splitlines())
    mountain = [line for line in INPUT.splitlines()]

    # print(f"Width:  {width_of_mountain}")
    # print(f"Bottom: {bottom_of_mountain}")

    while elevation + down <= bottom_of_mountain - 1:

        try:
            longitude += across

            if longitude >= width_of_mountain:
                longitude -= width_of_mountain

            if mountain[elevation+down][longitude] == '#':
                trees_encountered += 1
            else:
                open_spaces += 1

            elevation += down
        except IndexError as e:
            pdb.set_trace()

    # print(f"Trees Hit:   {trees_encountered}")
    # print(f"Open Spaces:   {open_spaces}")

    return trees_encountered

def solve_part_two():

    trees_hit = []
    slope_combinations = [
        [1, 1],
        [3, 1],
        [5, 1],
        [7, 1],
        [1, 2]
    ]

    for combination in slope_combinations:
        trees = solve_part_one(combination[0], combination[1])
        print(trees)
        trees_hit.append(trees)
    
    result = reduce(lambda x, y: x*y, trees_hit)

    print(result)



def main():
    # solve_part_one()
    solve_part_two()



if __name__ == '__main__':
    main()