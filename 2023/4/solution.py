from input import INPUT_DATA

DEBUG = False

class Card:
    NUM = "num"
    WIN_NUMS = "winning"
    NUMBERS = "numbers"


def parse_card_data(input_data):
    card_data = {}

    for line in input_data.replace("  ", " ").splitlines():
        card_title, numbers_text = line.split(": ")
        card_number = int(card_title.split("Card")[1])
        winning_number_text, card_numbers_text = numbers_text.split(" | ")
        winning_numbers = [int(num_text) for num_text in winning_number_text.split(" ")]
        card_numbers = [int(num_text) for num_text in card_numbers_text.split(" ")]

        card_data[card_number] = {
            Card.NUM: card_number,
            Card.WIN_NUMS: winning_numbers,
            Card.NUMBERS: card_numbers 
        }

    return card_data


def solve_part_one():
    total_points = 0
    card_data = parse_card_data(INPUT_DATA)

    for number, card in card_data.items():
        points = 0
        winning_numbers = 0
        for number in card[Card.NUMBERS]:
            if number in card[Card.WIN_NUMS]:
                winning_numbers += 1

        if winning_numbers > 0:
            points = 1
            for _ in range(winning_numbers - 1):
                points *= 2

        if DEBUG:
            print(f"Card {number}:  {points}")

        total_points += points

    return total_points


def solve_part_two():
    card_data = parse_card_data(INPUT_DATA)

    cards_by_number = {
        card[Card.NUM]: [card]
        for card in card_data.values()
    }
    current_number = 1

    while current_number <= 198:  # lol I'm lazy
        for _ in range(len(cards_by_number[current_number])):
            original_card = card_data[current_number]
            winning_numbers = 0
            for number in original_card[Card.NUMBERS]:
                if number in original_card[Card.WIN_NUMS]:
                    winning_numbers += 1

            for copy_num in range(1, winning_numbers + 1):
                duplicate_number = current_number + copy_num
                # print(f"Cur: {current_number} | Adding Card to:   {duplicate_number}")
                duplicate_card = card_data[duplicate_number]
                cards_by_number[duplicate_number].append(duplicate_card)
                # print(cards_by_number[duplicate_number])
            # print(f"[{current_number}]Cards Added: {winning_numbers}")

        current_number += 1

    total_cards = 0
    for cards in cards_by_number.values():
        total_cards += len(cards)

    return total_cards


def main():
    print(f"Answer 1:     {solve_part_one()}")
    print(f"Answer 2 (Slow):     {solve_part_two()}")


if __name__ == "__main__":
    main()