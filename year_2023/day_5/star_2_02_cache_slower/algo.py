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
from bisect import bisect_right
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm

from year_2023.day_5.star_1.algo import Data, get_highway, parse, START_NAME

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"


CACHE = defaultdict(dict)


def get_seed_location(data: Data, highway: list[str], seed: int) -> int:
    pair = [None, START_NAME]
    value = seed

    pairs = []

    for next_name in highway[1:]:
        pair = (pair[1], next_name)

        cr = CACHE[next_name].get(value)
        if cr is not None:
            value = cr
            break

        pairs.append((next_name, value))

        mappings = data.mapping[pair]
        index = bisect_right(mappings, value, key=lambda el: el[0])

        if index != 0:
            mapping = mappings[index - 1]
            if mapping[0] + mapping[2] >= value:
                value = mapping[1] + value - mapping[0]

    for name, start_value in pairs:
        CACHE[name][start_value] = value

    return value


def algo(text: str) -> int:
    data = parse(text)
    highway = get_highway(data.mapping.keys())

    locations = []
    it = iter(data.seeds)
    print(len(data.seeds) / 2)

    for seed in it:
        length = next(it)
        print("start", seed, length)

        with tqdm(total=length) as pbar:
            while length:
                # print(seed)
                locations.append(get_seed_location(data, highway, seed))

                seed += 1
                length -= 1
                pbar.update(1)
                pbar.set_description(f"Size={sys.getsizeof(CACHE)}")

    return min(locations)


def main():
    text = input_data_file.read_text()
    result = algo(text)
    print(result)


if __name__ == "__main__":
    main()
