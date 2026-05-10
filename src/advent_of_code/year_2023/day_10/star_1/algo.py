"""
--- Day 10: Pipe Maze ---

You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal
island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so
you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do
occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction;
maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire
some metal grass, you notice something metallic scurry away in your peripheral vision and jump into
a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need
to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with
pipes; it was hard to tell at first because they're the same metallic silver color as the "ground".
You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't
    show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal
is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like
this:

.....
.S-7.
.|.|.
.L-J.
.....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the
adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the
same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones
connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in
the main loop connects to its two neighbors (including S, which will have exactly two pipes
connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest
from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this
by direct distance. Instead, you need to find the tile that would take the longest number of steps
along the loop to reach from the starting point - regardless of which way around the loop the animal
went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....

You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....

In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the
starting position to the point farthest from the starting position?
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
