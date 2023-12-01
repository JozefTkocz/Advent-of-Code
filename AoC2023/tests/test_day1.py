import pytest

from aoc2023.day_1 import (
    sum_calibration_values,
    replace_first_letters_of_number_words_with_ints,
    first_and_last_ints_or_words,
    first_and_last_int_characters,
)


def test_sum_calibration_doc():
    input_data = """1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet"""

    expected_result = 142
    assert (
        sum_calibration_values(input_data.split("\n"), first_and_last_int_characters)
        == expected_result
    )


def test_sum_calibration_doc_with_strings():
    input_data = """two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen"""

    assert (
        sum_calibration_values(input_data.split("\n"), first_and_last_ints_or_words)
        == 281
    )


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("35", "35"),
        ("two1nine", "2wo19ine"),
        ("eightwothree", "8igh2wo3hree"),
        ("abcone2threexyz", "abc1ne23hreexyz"),
        ("xtwone3four", "x2w1ne34our"),
        ("4nineeightseven2", "49ine8ight7even2"),
        ("zoneight234", "z1n8ight234"),
        ("7pqrstsixteen", "7pqrst6ixteen"),
        ("sevenine", "7eve9ine"),
    ],
)
def test_replace_substrings_with_numbers(test_input, expected):
    assert replace_first_letters_of_number_words_with_ints(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76),
    ],
)
def test_get_line_value_ints_or_strings(test_input, expected):
    assert first_and_last_ints_or_words(test_input) == expected
