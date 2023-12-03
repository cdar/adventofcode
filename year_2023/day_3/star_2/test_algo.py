from textwrap import dedent

from .algo import algo


def test_algo():
    assert (
        algo(
            dedent(
                """\
                467..114..
                ...*......
                ..35..633.
                ......#...
                617*......
                .....+.58.
                ..592.....
                ......755.
                ...$.*....
                .664.598..
                """
            ),
        )
        == [16345, 451490]
    )
