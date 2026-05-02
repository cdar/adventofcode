from textwrap import dedent

from .algo import algo, parse


def test_algo():
    assert (
        algo(
            *parse(
                dedent(
                    """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
                """
                ),
            )
        )
        == 288
    )
