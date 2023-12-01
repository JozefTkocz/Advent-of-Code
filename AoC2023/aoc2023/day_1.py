from typing import Callable

STRING_NUMBER_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def sum_calibration_values(lines: list[str], evaluate_line: Callable) -> int:
    return sum([evaluate_line(l) for l in lines])


def replace_first_letters_of_number_words_with_ints(line: str) -> str:
    for idx in range(len(line)):
        for word, number in STRING_NUMBER_MAP.items():
            if is_word_at_index(string=line, word=word, idx=idx):
                line = replace_char_at_index(idx=idx, string=line, new_char=number)
    return line


def is_word_at_index(string: str, word: str, idx: int) -> bool:
    return string[idx : idx + len(word)] == word


def replace_char_at_index(idx: int, string: str, new_char: str):
    return string[:idx] + new_char + string[idx + 1 :]


def first_and_last_ints_or_words(line: str) -> int:
    return first_and_last_int_characters(
        replace_first_letters_of_number_words_with_ints(line)
    )


def first_and_last_int_characters(line: str) -> int:
    first_number = 0
    last_number = 0
    for char in line:
        if char.isnumeric():
            first_number = char
            break
    for char in line[::-1]:
        if char.isnumeric():
            last_number = char
            break
    calibration_value = int(f"{first_number}{last_number}")
    return calibration_value


if __name__ == "__main__":
    with open("../tests/test_data/day_1_input.txt") as file:
        input_data = file.read().split("\n")

    part_1 = sum_calibration_values(input_data, first_and_last_int_characters)
    part_2 = sum_calibration_values(input_data, first_and_last_ints_or_words)

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
