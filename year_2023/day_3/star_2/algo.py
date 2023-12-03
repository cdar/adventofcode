"""
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear
is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the
result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the
engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

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

In this schematic, there are two gears. The first is in the top left; it has part
numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right;
its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only
adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""
from pathlib import Path

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"


SYMBOLS = "*"


def _get_number(data: list[str], cord: tuple[int, int]) -> str:
    digits = []
    for char in data[cord[0]][cord[1] :]:
        if char.isdigit():
            digits.append(char)
        else:
            break
    return "".join(digits)


def algo(data: str) -> list[int]:
    data = data.splitlines()
    max_x = len(data[0])
    max_y = len(data)

    y = 0
    asterisk_to_numbers: dict[tuple[int, int], set[tuple[int, int]]] = {}

    while y < max_y:
        number_index: int = -1
        x = 0

        while x < max_x:
            if data[y][x].isdigit():
                if number_index == -1:
                    number_index = x

                for _cord in [
                    [-1, -1],
                    [-1, 0],
                    [-1, 1],
                    [0, -1],
                    [0, 1],
                    [1, -1],
                    [1, 0],
                    [1, 1],
                ]:
                    cord = y + _cord[0], x + _cord[1]
                    if -1 in cord or cord[0] >= max_y or cord[1] >= max_x:
                        continue
                    if data[cord[0]][cord[1]] in SYMBOLS:
                        asterisk_to_numbers.setdefault(cord, set()).add(
                            (y, number_index)
                        )
                        break
            else:
                number_index = -1

            x += 1

        y += 1

    result = []
    for numbers_cords in asterisk_to_numbers.values():
        if len(numbers_cords) == 2:
            result.append(
                int(_get_number(data, numbers_cords.pop()))
                * int(_get_number(data, numbers_cords.pop()))
            )

    return result


def main():
    text = input_data_file.read_text()
    result = algo(text)
    print(result)
    print("sum:", sum(result))


if __name__ == "__main__":
    main()
