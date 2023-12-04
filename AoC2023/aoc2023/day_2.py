from dataclasses import dataclass


@dataclass
class Game:
    id: int
    colour_sets: list[dict]


COLOURS = ["red", "green", "blue"]


def parse_input(input_data: str) -> list[Game]:
    return [parse_game(g) for g in input_data.split("\n")]


def parse_game(input_line: str) -> Game:
    game_id = int(input_line.split(":")[0].split("Game")[1])
    set_input = input_line.split(":")[1].replace(" ", "").split(";")

    sets = []
    for set_data in set_input:
        input_data = {}

        for colour_group in set_data.split(","):
            for colour in COLOURS:
                if colour in colour_group:
                    number = int(colour_group.split(colour)[0])
                    input_data.update({colour: number})
        sets.append(input_data)

    return Game(id=game_id, colour_sets=sets)


def is_possible(subset_collection: list[dict], colour_set: dict) -> bool:
    allowed_colours = set(colour_set.keys())

    for colour, number in colour_set.items():
        for subset in subset_collection:
            for key in subset.keys():
                if key not in allowed_colours:
                    return False

            subset_number = subset.get(colour) or 0
            if subset_number > number:
                return False
    return True


def evaluate_part_1(games: list[Game], colour_set: dict) -> int:
    total = 0

    for game in games:
        if is_possible(game.colour_sets, colour_set):
            total += game.id

    return total


def get_minimum_colour_set(game: Game) -> dict:
    minimum_set = {}

    for colour_set in game.colour_sets:
        for colour, number in colour_set.items():
            minimum = minimum_set.get(colour)
            if not minimum:
                minimum_set.update({colour: number})
            if minimum_set.get(colour) < number:
                minimum_set.update({colour: number})
    return minimum_set


def evaluate_power(colour_set: dict) -> int:
    result = 1
    for colour, number in colour_set.items():
        result *= number
    return result


def evaluate_part_2(games: list[Game]) -> int:
    total = 0

    for game in games:
        minimum_set = get_minimum_colour_set(game)
        total += evaluate_power(minimum_set)

    return total


if __name__ == "__main__":
    with open("../tests/test_data/day_2_input.txt") as file:
        input_data = file.read()

    games_list = parse_input(input_data)

    part_1 = evaluate_part_1(games_list, {"red": 12, "green": 13, "blue": 14})
    part_2 = evaluate_part_2(games_list)

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
