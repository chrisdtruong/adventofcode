from collections import defaultdict
from input import INPUT_DATA


def game_line_parser(line):
    """Given a line, parse it to provide the game number and the rounds"""
    game_text, round_text = line.split(": ")
    game_number = game_text.split(" ")[1]
    game_results = defaultdict(list)
    grab_count = 0
    for grab_results in round_text.split("; "):
        cube_results = grab_results.split(", ")
        for cubes in cube_results:
            count, color = cubes.split(" ")
            game_results[grab_count].append({color: int(count)})
        grab_count += 1

    return game_number, game_results


def get_max_pull_per_color(game_results):
    max_pull_count = {}
    for pull_round in game_results.values():
        for pull in pull_round:
            for color, count in pull.items():
                if color not in max_pull_count:
                    max_pull_count[color] = 0

                if count > max_pull_count[color]:
                    max_pull_count[color] = count

    return max_pull_count


def solve_part_one():
    bag_definition = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    games = INPUT_DATA.splitlines()
    valid_games = []

    for game in games:
        game_number, game_results = game_line_parser(game)
        max_pull_count = get_max_pull_per_color(game_results)
        if all(
            [
                count <= bag_definition[color]
                for color, count in max_pull_count.items()
            ]
        ):
            valid_games.append(int(game_number))

    answer = 0
    for game in valid_games:
        answer += game

    print(f"Answer:  {answer}")


def get_minimum_cubes_required(game_results):
    minimum_pull_count = {}
    for pull_round in game_results.values():
        for pull in pull_round:
            for color, count in pull.items():
                if color not in minimum_pull_count:
                    minimum_pull_count[color] = count

                if count >= minimum_pull_count[color]:
                    minimum_pull_count[color] = count

    return minimum_pull_count


def solve_part_two():
    games = INPUT_DATA.splitlines()
    answer = 0

    for game in games:
        game_number, game_results = game_line_parser(game)
        max_pull_count = get_max_pull_per_color(game_results)
        
        min_pull_numbers = max_pull_count.values()
        game_power = 1
        for num in min_pull_numbers:
            game_power *= num
        
        answer += game_power

    print(f"Answer: {answer}")


def main():
    solve_part_one()
    solve_part_two()


if __name__ == "__main__":
    main()