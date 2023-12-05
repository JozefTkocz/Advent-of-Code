from aoc2023.day_4 import score_card


def test_score_card():
    """41 48 83 86 17 | 83 86  6 31 17  9 48 53"""

    assert score_card([41, 48, 83, 86, 17], [83, 86, 6, 31, 17, 9, 48, 53]) == 8
