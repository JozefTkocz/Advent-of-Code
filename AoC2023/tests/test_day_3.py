from aoc2023.day_3 import (
    convert_input_to_array,
    get_chars_adjacent_to_symbols,
    get_min_max,
    propagate_consecutive_bools,
    get_chars_at_positions,
)


def test_get_chars_at_position():
    positions = [True, True, False, False, True, True]
    string = "aabbcc"
    assert get_chars_at_positions(string, positions) == ["aa", "cc"]

    positions = [True, True, True, False, False, True, True, True, False, False]
    string = "467..114.."
    assert get_chars_at_positions(string, positions) == ["467", "114"]


def test_get_adjacent_numbers_in_line():
    inpt = [None, None, None, None, None, None, True, False, False, None]
    expected = [None, None, None, None, None, None, True, True, True, None]
    assert propagate_consecutive_bools(inpt) == expected

    inpt = [False, False, True, None, False, False, False, None, None]
    expected = [True, True, True, None, False, False, False, None, None]
    assert propagate_consecutive_bools(inpt) == expected

    inpt = [None] * 10
    expected = [None] * 10
    assert propagate_consecutive_bools(inpt) == expected

    inpt = [False] * 10
    expected = [False] * 10
    assert propagate_consecutive_bools(inpt) == expected

    inpt = [False, True, True, None, False, False, True, None, None]
    expected = [True, True, True, None, True, True, True, None, None]
    assert propagate_consecutive_bools(inpt) == expected

    inpt = [False, True, True, None, False, False, True, False, None]
    expected = [True, True, True, None, True, True, True, True, None]
    assert propagate_consecutive_bools(inpt) == expected

    inpt = [False, True, True, None, False, False, True, False, False]
    expected = [True, True, True, None, True, True, True, True, True]
    assert propagate_consecutive_bools(inpt) == expected


def test_get_min_max():
    assert get_min_max(0, 3) == (0, 1)
    assert get_min_max(1, 3) == (0, 2)
    assert get_min_max(2, 3) == (1, 3)
    assert get_min_max(3, 3) == (2, 3)

    assert get_min_max(0, 6) == (0, 1)
    assert get_min_max(0, 5) == (0, 1)


def test_get_symbol_adjacency():
    inpt = """...
        ...
        ..."""
    arr = convert_input_to_array(inpt)
    assert get_chars_adjacent_to_symbols(arr) == []

    inpt = """.+.
            .1.
            ..."""
    arr = convert_input_to_array(inpt)
    assert get_chars_adjacent_to_symbols(arr) == [(1, 1)]

    inpt = """..+
    .1.
    ..."""
    arr = convert_input_to_array(inpt)
    assert get_chars_adjacent_to_symbols(arr) == [(1, 1)]
    inpt = """1....*1
    *...... 
    ...1...
    .......
    .*...*.
    1.....1"""
    arr = convert_input_to_array(inpt)
    assert get_chars_adjacent_to_symbols(arr) == [(0, 0), (0, 6), (5, 0), (5, 6)]
