"""
Your calculation isn't quite right. It looks like some of the digits are actually
spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also
count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit
on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these
together produces 281.

What is the sum of all of the calibration values?
"""
from pathlib import Path

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"


DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

DIGITS_REVERSED = {"".join(reversed(k)): v for k, v in DIGITS.items()}


def get_digit(revers: bool = False):
    chars = ""
    digits = DIGITS_REVERSED if revers else DIGITS

    def _get_digit(char: str):
        if char.isdigit():
            return char
        nonlocal chars
        chars += char

        for digit_word in digits:
            if digit_word in chars:
                return digits[digit_word]

    return _get_digit


def algo(data: str | list[str]) -> list[int]:
    if isinstance(data, str):
        data = data.splitlines()

    result = []
    for line in data:
        n = int(
            next(filter(None, map(get_digit(), line)))
            + next(filter(None, map(get_digit(True), reversed(line))))
        )
        result.append(n)

    return result


if __name__ == "__main__":
    result = algo(input_data_file.read_text())
    print(result)
    print("sum:", sum(result))
