"""
The engine schematic (your puzzle input) consists of a visual representation of the
engine. There are lots of numbers and symbols you don't really understand, but
apparently any number adjacent to a symbol, even diagonally, is a "part number" and
should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

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

In this schematic, two numbers are not part numbers because they are not adjacent to a
symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a
symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the
part numbers in the engine schematic?
"""
from pathlib import Path

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"


SYMBOLS = "#$%&*+-/=@"


def get_symbols(text: str) -> str:
    symbols = set()
    for char in text:
        if char.isdigit() or char in [" ", "\n", "."]:
            continue
        symbols.add(char)
    return "".join(sorted(symbols))


def algo(data: str) -> list[int]:
    data = data.splitlines()
    max_x = len(data[0])
    max_y = len(data)

    y = 0
    result = []

    while y < max_y:
        number_index: int = -1
        adjacent_to_symbol = False
        x = 0

        while x < max_x:
            if data[y][x].isdigit():
                if number_index == -1:
                    number_index = x
                if not adjacent_to_symbol:
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
                        cord = [y + _cord[0], x + _cord[1]]
                        if -1 in cord or cord[0] >= max_y or cord[1] >= max_x:
                            continue
                        if data[cord[0]][cord[1]] in SYMBOLS:
                            adjacent_to_symbol = True
                            break
            else:
                if number_index != -1 and adjacent_to_symbol:
                    result.append(int(data[y][number_index:x]))

                number_index = -1
                adjacent_to_symbol = False

            x += 1

        if number_index != -1 and adjacent_to_symbol:
            result.append(int(data[y][number_index:x]))

        y += 1

    return result


if __name__ == "__main__":
    text = input_data_file.read_text()
    # symbols = get_symbols(text)
    # print(f"{symbols=}")
    result = algo(text)
    print(result)
    print("sum:", sum(result))
