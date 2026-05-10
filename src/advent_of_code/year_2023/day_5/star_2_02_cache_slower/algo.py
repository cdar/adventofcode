import sys
from bisect import bisect_right
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm

from advent_of_code.year_2023.day_5.star_1.algo import (
    Data,
    get_highway,
    parse,
    START_NAME,
)

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "../star_1/input.txt"


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

        mappings = data.mappings[pair]
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
    highway = get_highway(data.mappings.keys())

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
    print("expected: 81956384")


if __name__ == "__main__":
    main()
