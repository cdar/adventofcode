"""
--- Part Two ---

You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is
within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate
how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........

The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast
(marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop
again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....

In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside
the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still
outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........

In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...

The above sketch has many random bits of ground, some of which are in the loop (I) and some of which
are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO

In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another
example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How
many tiles are enclosed by the loop?
"""

from enum import IntEnum
import typing as t
from dataclasses import dataclass
from pathlib import Path

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"


class Direction(IntEnum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


@dataclass
class InputData:
    width: int
    height: int
    plan: str
    start_x: int
    start_y: int
    start_directions: list[Direction]


def _pipe_to_directions(pipe: str) -> list[Direction]:
    directions = []
    if pipe in "-J7":
        directions.append(Direction.LEFT)
    if pipe in "|LJ":
        directions.append(Direction.UP)
    if pipe in "-LF":
        directions.append(Direction.RIGHT)
    if pipe in "|7F":
        directions.append(Direction.DOWN)
    return directions


def _calc_directions_from_pipe_neighbors(
    width: int, height: int, plan: str, x: int, y: int
) -> list[Direction]:
    directions = []

    if x > 1 and plan[y * width + x - 1] in "-LF":
        directions.append(Direction.LEFT)
    if y > 1 and plan[(y - 1) * width + x] in "|7F":
        directions.append(Direction.UP)
    if x + 1 < width and plan[y * width + x + 1] in "-J7":
        directions.append(Direction.RIGHT)
    if y + 1 < height and plan[(y + 1) * width + x] in "|LJ":
        directions.append(Direction.DOWN)

    return directions


def parse(text: str) -> InputData:
    width = text.find("\n")
    height = text.count("\n") + 1
    plan = text.replace("\n", "")

    n_start = plan.find("S")
    start_yx = divmod(n_start, width)
    assert plan[start_yx[0] * width + start_yx[1]] == "S"

    start_directions = _calc_directions_from_pipe_neighbors(
        width, height, plan, start_yx[1], start_yx[0]
    )

    return InputData(width, height, plan, start_yx[1], start_yx[0], start_directions)


OPPOSITE_DIRECTIONS = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]


def _go_next(
    input_data: InputData, x, y, direction: Direction
) -> tuple[int, int, Direction]:
    match direction:
        case Direction.LEFT:
            x -= 1
        case Direction.UP:
            y -= 1
        case Direction.RIGHT:
            x += 1
        case Direction.DOWN:
            y += 1
    next_directions = _pipe_to_directions(input_data.plan[input_data.width * y + x])
    return (
        x,
        y,
        next_directions[
            0 if next_directions.index(OPPOSITE_DIRECTIONS[direction]) == 1 else 1
        ],
    )


def algo(input_data: InputData) -> int:
    walker_0 = (input_data.start_x, input_data.start_y, input_data.start_directions[0])
    walker_1 = (input_data.start_x, input_data.start_y, input_data.start_directions[1])
    distance = 0

    while True:
        walker_0 = _go_next(input_data, *walker_0)
        walker_1 = _go_next(input_data, *walker_1)
        distance += 1

        if walker_0[0] == walker_1[0] and walker_0[1] == walker_1[1]:
            return distance


def start(intput: str) -> int:
    return algo(parse(intput))


def main():
    print("first... ")
    assert 4 == start(
        """.....
.S-7.
.|.|.
.L-J.
    ....."""
    )
    print("ok")

    print("second... ")
    assert 8 == start(
        """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
    )
    print("ok")

    print("third... ")
    text = input_data_file.read_text()
    print(start(text))
    print("expected: 6947")


if __name__ == "__main__":
    main()
