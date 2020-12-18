import pdb
import re
from itertools import takewhile

from input import INPUT


def get_list_of_rules() -> list:
    return INPUT.split('\n')


def process_rule(rule: str) -> dict:
    rule_components = rule.split(' contain ')
    holding_bag = rule_components[0].rstrip('s')

    if rule_components[1] == 'no other bags.':
        bag_rules = []
    else:
        bag_rules = rule_components[1].split(',')
        # Remove Trailing .
        bag_rules[-1] = bag_rules[-1].rstrip('.')
        # Remove trailing S
        bag_rules = [rule.rstrip('s') for rule in bag_rules]
        # Remove Starting space
        bag_rules = [rule.lstrip(' ') for rule in bag_rules]
        

        bag_rules = [{
            'color': rule[2:],
            'count': int(rule[0])
        } for rule in bag_rules]

    return {
        'color': holding_bag,
        'rules': bag_rules 
    }


def recursive_calculate_bag_depth_and_count(bag: dict, rules: list) -> int:
    for rule in rules:
        if rule['color'] == bag['color']:
            if len(rule['rules']) == 0:
                return bag['count']
            else:
                total_bags = 0
                for next_rule in rule['rules']:
                    count = recursive_calculate_bag_depth_and_count(next_rule, rules)
                    total_bags += bag['count'] * count
                
                return total_bags + bag['count']
        else:
            pass


def solve_part_one() -> int:
    rules = get_list_of_rules()
    bag_rules = [process_rule(rule) for rule in rules]

    hold_level = 0
    possible_bag_levels = [['shiny gold bag']]
    found_bag = True

    while found_bag is True:
        found_bag = False
        possible_bag_levels.append([])
        for target_bag in possible_bag_levels[hold_level]:
            for bag in bag_rules:
                for rule in bag['rules']:
                    if rule['color'] == target_bag:
                        possible_bag_levels[hold_level+1].append(bag['color'])
                        found_bag = True

        hold_level += 1

    del possible_bag_levels[0]

    flat_bag_list = set([bag for bag_level in possible_bag_levels for bag in bag_level])

    return len(flat_bag_list)


def solve_part_two() -> int:
    rules = get_list_of_rules()
    bag_rules = [process_rule(rule) for rule in rules]


    top_level_bags = []

    for bag in bag_rules:
        if bag['color'] == 'shiny gold bag':
            for rule in bag['rules']:
                top_level_bags.append(rule)

    total_count = 0
    for bag in top_level_bags:
        total_count += recursive_calculate_bag_depth_and_count(bag, bag_rules)

    return total_count


def main() -> None:
    print(f"Part One:   {solve_part_one()}")
    print(f"Part Two:   {solve_part_two()}")


if __name__ == '__main__':
    main()