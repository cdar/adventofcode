from textwrap import dedent

import pytest

from .algo import algo


@pytest.mark.parametrize(
    "text, expected_results",
    [
        (
            """\
            broadcaster -> a, b, c
            %a -> b
            %b -> c
            %c -> inv
            &inv -> a
            """,
            (8000, 4000),
        ),
        (
            """\
            broadcaster -> a
            %a -> inv, con
            &inv -> b
            %b -> con
            &con -> output
            """,
            (4250, 2750),
        ),
    ],
)
def test_algo(text, expected_results):
    assert (
        algo(
            dedent(text),
        )
        == expected_results
    )
