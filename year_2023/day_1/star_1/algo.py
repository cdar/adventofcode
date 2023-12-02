"""
The newly-improved calibration document consists of lines of text; each line originally
contained a specific calibration value that the Elves now need to recover. On each line,
the calibration value can be found by combining the first digit and the last digit (in
that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77.
Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration
values?
"""
from pathlib import Path

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"


def algo(data: str | list[str]) -> list[int]:
    if isinstance(data, str):
        data = data.splitlines()

    result = []
    for line in data:
        n = int(
            next(filter(str.isdigit, line)) + next(filter(str.isdigit, reversed(line)))
        )
        result.append(n)

    return result


if __name__ == "__main__":
    result = algo(input_data_file.read_text())
    print(result)
    print("sum:", sum(result))
