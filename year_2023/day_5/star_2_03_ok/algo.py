"""
Everyone will starve if you only plant such a small number of seeds. Re-reading the
almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value
is the start of the range and the second value is the length of the range. So, in the
first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first
range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second
range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed
numbers.

In the above example, the lowest location number can be obtained from seed number 82,
which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45,
humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the
almanac. What is the lowest location number that corresponds to any of the initial seed
numbers?
"""
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Iterable, Any

from tqdm import tqdm

from year_2023.day_5.star_1.algo import Data, get_highway, parse, START_NAME

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"


def batched(iterable: Iterable[Any], n: int = 2) -> Iterable[list[Any]]:
    assert n > 0
    i = 0
    b = []
    for el in iterable:
        b.append(el)
        i += 1
        if i == n:
            yield b
            b = []
            i = 0
    if b:
        yield b


def get_next_solutions(
    points: list[list[int]], mappings: list[list[int]]
) -> list[list[int]]:
    results = []
    i_mapping = 0

    # fmt: off
    for point in points:
        while i_mapping < len(mappings):
            if point[0] < mappings[i_mapping][0]:
                if point[1] < mappings[i_mapping][0]:
                    results.append(point)
                    break
                else:
                    results.append([point[0], mappings[i_mapping][0] - 1])
                    point = [mappings[i_mapping][0], point[1]]
                    # i_mapping += 1
            elif point[0] <= mappings[i_mapping][1]:
                if point[1] <= mappings[i_mapping][1]:
                    results.append([
                        point[0] - mappings[i_mapping][0] + mappings[i_mapping][2],
                        point[1] - mappings[i_mapping][0] + mappings[i_mapping][2]
                    ])
                    break
                else:
                    results.append([
                        point[0] - mappings[i_mapping][0] + mappings[i_mapping][2],
                        mappings[i_mapping][1] - mappings[i_mapping][0] + mappings[i_mapping][2]
                    ])
                    point = [mappings[i_mapping][1] + 1, point[1]]
                    # i_mapping += 1
            else:
                i_mapping += 1

        if i_mapping == len(mappings):
            results.append(point)
    # fmt: on

    return results


def algo(text: str) -> int:
    data = parse(text)

    for mappings in data.mappings.values():
        for mapping in mappings:
            mapping[:] = [mapping[0], mapping[0] + mapping[2] - 1, mapping[1]]

    highway = get_highway(data.mappings.keys())

    def _sort(array):
        array.sort(key=lambda el: el[0])
        return array

    solutions: list[list[int]] = [
        [x, x + length - 1] for x, length in batched(data.seeds)
    ]

    for pair in pairwise(highway):
        # print(pair)
        solutions = get_next_solutions(_sort(solutions), _sort(data.mappings[pair]))

    _sort(solutions)

    return solutions[0][0]


def main():
    text = input_data_file.read_text()
    result = algo(text)
    print(result)


if __name__ == "__main__":
    main()
