from textwrap import dedent

from .algo import algo


def test_algo():
    assert (
        algo(
            dedent(
                """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
                """
            )
        )
        == [29, 83, 13, 24, 42, 14, 76]
    )
