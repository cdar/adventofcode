from textwrap import dedent

import pytest

from .algo import algo, get_next_solutions


TEST_DATA = dedent(
    """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
)

TEST_DATA_STEPS_RESULTS = [
    # seeds:  79 - 92, 55 - 67
    # source: 98 - 99, 50 - 97
    # target: 50 - 51, 52 - 99
    # 79+2 - 92+2, 55+2 - 67+2
    [[57, 69], [81, 94]],
    # soil
    # source: 15 - 51, 52 - 53, 0 - 14
    # target: 0 - 36, 37 - 38, 39 - 53
    [[57, 69], [81, 94]],
    # fertilizer
    # source: 53 - 60, 11 - 51, 0 - 6, 7 - 10
    # target: 49 - 57, 0 - 41, 42 - 48, 57 - 60
    # [],
    # water
    # source:
    # target:
    # [],
    # light
    # source:
    # target:
    # [],
    # temperature
    # source:
    # target:
    # [],
    # humidity
    # source:
    # target:
    # [],
]


def test_algo_by_step(mocker):
    orig_get_next_solutions = get_next_solutions
    run = 0

    def _side_effect(points, mappings):
        nonlocal run
        result = orig_get_next_solutions(points, mappings)

        if run < len(TEST_DATA_STEPS_RESULTS):
            assert result == TEST_DATA_STEPS_RESULTS[run], run

        run += 1
        return result

    mocker.patch(
        "year_2023.day_5.star_2_03_ok.algo.get_next_solutions", side_effect=_side_effect
    )

    algo(TEST_DATA)


def test_algo():
    assert algo(TEST_DATA) == 46


@pytest.mark.parametrize(
    "points, mappings, result",
    [
        ([[2, 2]], [[3, 3, 5]], [[2, 2]]),  # 0
        ([[3, 3]], [[3, 3, 5]], [[5, 5]]),
        ([[4, 4]], [[3, 3, 5]], [[4, 4]]),
        ##################################
        ([[2, 3]], [[3, 3, 5]], [[2, 2], [5, 5]]),  # 3
        ([[3, 4]], [[3, 3, 5]], [[5, 5], [4, 4]]),
    ],
)
def test_get_next_solutions(points, mappings, result):
    assert get_next_solutions(points, mappings) == result
