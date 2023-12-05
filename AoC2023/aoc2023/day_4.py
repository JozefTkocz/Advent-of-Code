def score_card(winning_numbers: list[int], hand: list[int]):
    n = count_card_matches(hand, winning_numbers)
    if n:
        return 2 ** (n - 1)
    else:
        return 0


def count_card_matches(hand, winning_numbers) -> int:
    n = 0
    for number in hand:
        if number in winning_numbers:
            n += 1
    return n


def parse_input(card_string) -> tuple[list[int], list[int]]:
    numbers = card_string.split(":")[1].split("|")

    winning = numbers[0].split(" ")
    winning_numbers = [int(n) for n in winning if n != ""]

    hand = numbers[1].split(" ")
    hand_numbers = [int(n) for n in hand if n != ""]

    return winning_numbers, hand_numbers


def part_1(input_data: str) -> int:
    total = 0
    cards = input_data.split("\n")
    for card in cards:
        winning, hand = parse_input(card)
        total += score_card(winning, hand)

    return total


def part_2(input_data: str) -> int:
    return score_part_2(input_data.split("\n"))


def score_part_2(cards: list[str]) -> int:
    # pass through everything at least once
    evaluation_passes = {idx: 1 for idx in range(len(cards))}
    card_instances = {idx: 0 for idx in range(len(cards))}
    cards_to_process = len(cards)

    while cards_to_process > 0:
        for card_id, passes in evaluation_passes.items():
            if not passes:
                continue

            card_instances[card_id] += 1
            evaluation_passes[card_id] -= 1  # decrement as we pass through
            cards_to_process -= 1

            winning, hand = parse_input(cards[card_id])
            winning_cards = count_card_matches(hand, winning)
            cards_to_process += winning_cards

            for new_card in range(card_id + 1, card_id + 1 + winning_cards):
                evaluation_passes[new_card] += 1  # increment each winning card

    return sum(card_instances.values())


if __name__ == "__main__":
    with open("../tests/test_data/day_4_input.txt") as file:
        input_data = file.read()

    part_1 = part_1(input_data)
    part_2 = part_2(input_data)

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
