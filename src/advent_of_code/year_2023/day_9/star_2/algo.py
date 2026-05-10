"""
--- Part Two ---

Of course, it would be nice to have even more history included in your report. Surely it's safe to just extrapolate backwards as well, right?

For each history, repeat the process of finding differences until the sequence of differences is entirely zero. Then, rather than adding a zero to the end and filling in the next values of each previous sequence, you should instead add a zero to the beginning of your sequence of zeroes, then fill in new first values for each previous sequence.

In particular, here is what the third example history looks like when extrapolating back in time:

5  10  13  16  21  30  45
  5   3   3   5   9  15
   -2   0   2   4   6
      2   2   2   2
        0   0   0

Adding the new values on the left side of each sequence from bottom to top eventually reveals the new left-most history value: 5.

Doing this for the remaining example data above results in previous values of -3 for the first history and 0 for the second history. Adding all three new values together produces 2.

Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these extrapolated values?
"""

# 13:  2 -  2 =  0
# 12:  0 - -2 =  2 ->
# 11:  3 -  5 = -2
# 10: 10 -  5 =  5


# 13: 0
# 12: 2  -  0 =  2
# 11: 0  -  2 = -2
# 10: 3  - -2 =  5
#  9: 10 -  5 =  5

from pathlib import Path

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "../star_1/input.txt"


def parse(text: str) -> list[list[int]]:
    return [list(map(int, line.split())) for line in text.splitlines()]


def _calc_line(sequence: list[int]) -> int:
    steps: list[list[int]] = [sequence]
    i_step: int = 0

    while True:
        current_step = steps[i_step]
        new_step = []
        i_sequence: int = 1

        while i_sequence < len(current_step):
            new_step.append(current_step[i_sequence] - current_step[i_sequence - 1])
            i_sequence += 1

        for number in new_step:
            if number != 0:
                steps.append(new_step)
                i_step += 1
                break
        else:
            break

    last_number = 0
    for step in steps[::-1]:
        last_number = step[0] - last_number

    return last_number


def algo(input_data: list[list[int]]) -> int:
    result = 0
    for sequence in input_data:
        result += _calc_line(sequence)
    return result


def start(intput: str) -> int:
    return algo(parse(intput))


def main():
    print("first... ")
    assert 2 == start(
        """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    )
    print("ok")

    print("second... ")
    text = input_data_file.read_text()
    print(start(text))
    print("expected: 975")


if __name__ == "__main__":
    main()
