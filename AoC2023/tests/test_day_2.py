from aoc2023.day_2 import (
    Game,
    parse_game,
    is_possible,
    parse_input,
    evaluate_part_1,
    evaluate_part_2,
    get_minimum_colour_set,
)


def test_parse_input():
    input_text = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    result = parse_input(input_text)
    assert isinstance(result[0], Game)
    assert len(result) == 5


def test_parse_game():
    input_data = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"

    expected_sets = [
        {"blue": 3, "red": 4},
        {"red": 1, "green": 2, "blue": 6},
        {"green": 2},
    ]

    expected_result = Game(id=1, colour_sets=expected_sets)
    assert parse_game(input_data) == expected_result


def test_is_possible_extra_colour():
    subsets = [{"red": 1, "green": 1}]
    assert not is_possible(subsets, {"blue": 1})


def test_is_possible_too_many():
    subsets = [{"red": 2, "green": 1}]
    assert not is_possible(subsets, {"red": 1})


def test_is_possible_valid_subsets():
    subsets = [
        {"red": 3, "green": 3},
        {
            "red": 1,
        },
        {"green": 1},
    ]
    assert is_possible(subsets, {"red": 3, "green": 3})


def test_is_possible_example_set():
    subsets = [{"blue": 3, "red": 4}, {"red": 1, "green": 2, "blue": 6}, {"green": 2}]
    example_set = {"red": 12, "green": 13, "blue": 14}
    assert is_possible(subsets, example_set)


def test_example_input_pt_1():
    input_text = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    games_list = parse_input(input_text)
    assert evaluate_part_1(games_list, {"red": 12, "green": 13, "blue": 14}) == 8


def test_minimum_colour_set():
    input_game = Game(
        id=1,
        colour_sets=[
            {"blue": 3, "red": 4},
            {"red": 1, "green": 2, "blue": 6},
            {"green": 2},
        ],
    )
    result = get_minimum_colour_set(input_game)

    assert result == {"red": 4, "green": 2, "blue": 6}


def test_example_input_pt_2():
    input_text = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    games_list = parse_input(input_text)
    assert evaluate_part_2(games_list, {"red": 12, "green": 13, "blue": 14}) == 2286
