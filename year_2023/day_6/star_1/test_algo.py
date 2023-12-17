from textwrap import dedent

from .algo import algo, parse


def test_algo():
    assert (
        algo(
            *parse(
                dedent(
                    """\
Time:      7  15   30
Distance:  9  40  200
                """
                ),
            )
        )
        == 288
    )
