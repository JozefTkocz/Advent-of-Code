SYMBOLS = ["*", "#", "$", "+"]


def convert_input_to_array(schematic: str) -> list[list[str]]:
    lines = schematic.replace(" ", "").split("\n")

    elements = []
    for line in lines:
        elements.append([e for e in line])

    return elements


def is_symbol(c: str) -> bool:
    if c == ".":
        return False
    if c.isnumeric():
        return False
    return True


def get_chars_adjacent_to_symbols(array: list[list[str]]):
    cols = len(array[0])
    rows = len(array)
    coords_of_adjacent_numbers: list[tuple] = []

    for row in range(rows):
        for col in range(cols):
            # pass non numeric input
            if array[row][col].isnumeric():
                # account for array boundaries
                min_col, max_col = get_min_max(col, cols)
                min_row, max_row = get_min_max(row, rows)

                # look at all adjacency possibilities
                for neighbouring_line in range(min_row, min(max_row + 1, rows)):
                    for neighbouring_col in range(min_col, min(max_col + 1, cols)):
                        if is_symbol(array[neighbouring_line][neighbouring_col]):
                            coords_of_adjacent_numbers.append((row, col))

    return coords_of_adjacent_numbers


def get_numbers_on_each_line(input_lines: list[str], coords: list[tuple]):
    line_numbers: list[list[str]] = []
    for row, line in enumerate(input_lines):
        adjacent_coords = [c for c in coords if c[0] == row]

        def false_if_numeric(c):
            return False if c.isnumeric() else None

        bool_or_none = [false_if_numeric(c) for c in line]

        for a in adjacent_coords:
            bool_or_none[a[1]] = True

        adjacent_char_indices = propagate_consecutive_bools(bool_or_none)
        numbers = get_chars_at_positions(line, adjacent_char_indices)

        if numbers:
            line_numbers.append(numbers)

    return line_numbers


def get_chars_at_positions(string: str, indices: list[bool]) -> list[str]:
    results = []
    current_result = []
    for idx in range(len(indices)):
        if indices[idx]:
            current_result.append(string[idx])
        elif current_result and not indices[idx]:
            results.append("".join(current_result))
            current_result = []
        elif not indices[idx]:
            pass
    if current_result:
        results.append("".join(current_result))
    return results


def propagate_consecutive_bools(array: list[bool | None]) -> list[bool | None]:
    for idx in range(1, len(array) - 1):
        if array[idx]:
            # look backwards
            for s in range(idx - 1, -1, -1):
                if array[s] is None:
                    break
                elif array[s] is True:
                    pass
                elif array[s] is False:
                    array[s] = True

            # look forwards
            for sf in range(idx + 1, len(array)):
                if array[sf] is None:
                    break
                elif array[sf] is True:
                    pass
                elif array[sf] is False:
                    array[sf] = True

    return array


def get_min_max(idx: int, max_idx: int, step: int = 1):
    min_idx = max(0, idx - step)
    max_idx_ = min(idx + step, max_idx)
    return min_idx, max_idx_


def part_1(input_data: str) -> int:
    array = convert_input_to_array(input_data)
    coords_adjacent_to_symbols = get_chars_adjacent_to_symbols(array)
    numbers_per_line = get_numbers_on_each_line(
        input_data.split("\n"), coords_adjacent_to_symbols
    )

    total = 0
    for row in numbers_per_line:
        for number in row:
            total += int(number)

    return total


def find_gears(array: list[list[str]]) -> list[tuple]:
    gears = []
    for i, row in enumerate(array):
        for j, char in enumerate(row):
            if array[i][j] == "*":
                gears.append((i, j))
    return gears


def get_gear_ratio(coord: tuple, array: list[list[str]]):
    max_y = len(array)
    max_x = len(array[0])

    gear_y = coord[0]
    gear_x = coord[1]

    sub_y_min = max(gear_y - 1, 0)
    sub_y_max = min(gear_y + 2, max_y)  # plus 1 to make slicing work

    if gear_y == 0:
        sub_array = [["."] * max_x, array[0], array[1]]
    elif gear_y == max_y - 1:
        sub_array = [array[-2], array[-1], ["."] * max_x]
    else:
        sub_array = array[sub_y_min:sub_y_max]

    bool_array = [[None] * max_x, [None] * max_x, [None] * max_x]

    for i in range(3):
        for j in range(max_x):
            if sub_array[i][j].isnumeric():
                bool_array[i][j] = False

    min_col, max_col = get_min_max(gear_x, max_x)
    min_row, max_row = get_min_max(gear_y, 3)

    # look at all adjacency possibilities
    for neighbouring_line in range(0, 3):
        for neighbouring_col in range(min_col, min(max_col + 1, max_x)):
            if sub_array[neighbouring_line][neighbouring_col].isnumeric():
                # need to apply offset for gear coords
                if abs(neighbouring_col - gear_x) <= 1:
                    bool_array[neighbouring_line][neighbouring_col] = True

    all_numbers = []
    for row, line in enumerate(bool_array):
        adjacent_char_indices = propagate_consecutive_bools(line)
        numbers = get_chars_at_positions(sub_array[row], adjacent_char_indices)

        if len(numbers):
            all_numbers += numbers

    if len(all_numbers) == 2:
        return int(all_numbers[0]) * int(all_numbers[1])
    else:
        return 0


def part_2(input_data: str) -> int:
    array = convert_input_to_array(input_data)
    gears = find_gears(array)

    total = 0
    for gear in gears:
        total += get_gear_ratio(gear, array)

    return total


if __name__ == "__main__":
    with open("../tests/test_data/day_3_input.txt") as file:
        input_data = file.read()

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
