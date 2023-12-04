from textwrap import dedent

from .algo import algo


def test_algo():
    # fmt: off
    result = [
        1,  # 1 card - 4 matches
        1 + 1,  # 2 card - 2 matches
        1 + 1 + 2,  # 3 card - 2 matches
        1 + 1 + 2 + 4,  # 4 card - 1 match
        1 + 1 +     4 + 8, # 5 card - 0 match
        1
    ]
    # fmt: on

    assert sum(result) == 30

    assert (
        algo(
            dedent(
                """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
                """
            ),
        )
        == result
    )
