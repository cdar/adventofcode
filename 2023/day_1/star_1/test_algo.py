from textwrap import dedent

from .algo import algo


def test_algo():
    assert (
        algo(
            dedent(
                """\
                1abc2
                pqr3stu8vwx
                a1b2c3d4e5f
                treb7uchet
                """
            )
        )
        == [12, 38, 15, 77]
    )
