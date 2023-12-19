"""
the factory will also need a large supply of lava for a while; the Elves have already
started creating a large lagoon nearby for this purpose.

However, they aren't sure the lagoon will be big enough; they've asked you to take a
look at the dig plan (your puzzle input). For example:

R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)

The digger starts in a 1 meter cube hole in the ground. They then dig the specified
number of meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes
as they go. The directions are given as seen from above, so if "up" were north, then
"right" would be east, and so on. Each trench is also listed with the color that the
edge of the trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop of
trench (#) having been dug out from otherwise ground-level terrain (.):

#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######

At this point, the trench could contain 38 cubic meters of lava. However, this is just
the edge of the lagoon; the next step is to dig out the interior so that it is one meter
deep as well:

#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######

Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the
interior is dug out, the edges are also painted according to the color codes in the dig
plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig plan,
how many cubic meters of lava could it hold?
"""
from pathlib import Path

import pygame
from tqdm import tqdm

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"

SCALE = 10
# SCALE = 1
WHITE = 0xFFFFFF
GREEN = 0x00FF00

Plan = list[tuple[str, int]]


def parse(text: str) -> Plan:
    plan = []
    for line in text.splitlines():
        line = line.split()[:2]
        plan.append((line[0].lower(), int(line[1])))
    return plan


def draw_pixel(pxarray, y, x, color=WHITE):
    for _y in range(y * SCALE, y * SCALE + SCALE):
        for _x in range(x * SCALE, x * SCALE + SCALE):
            try:
                # print(f"{_x=} {_y=}")
                pxarray[_x, _y] = color
            except IndexError:
                # print(f"{_x=} {_y=}")
                raise


def print_area(area: list[list[str]]):
    print()
    for row in area:
        print("".join(row))


def algo(text: str) -> int:
    pygame.init()
    size = (800, 600)
    screen = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True

    screen.fill("black")
    pxarray = pygame.PixelArray(screen)
    pygame.display.flip()

    plan = parse(text)

    maxes = {
        direction: sum(map(lambda e: e[1], filter(lambda e: e[0] == direction, plan)))
        for direction in "lrud"
    }
    print(f"{maxes=}")
    n = max(maxes["l"] + maxes["r"], maxes["u"] + maxes["d"])
    n *= 3
    # n += 100
    start = n // 3
    # start = 50
    area = [["."] * n for _ in range(n)]

    print(f"{n=}")

    area[start][start] = "#"
    x, y = start, start

    draw_pixel(pxarray, y, x)

    while running:
        for direction, length in plan:
            while length > 0:
                match direction:
                    case "l":
                        x -= 1
                    case "r":
                        x += 1
                    case "u":
                        y -= 1
                    case "d":
                        y += 1
                area[y][x] = "#"
                length -= 1
                draw_pixel(pxarray, y, x)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # clock.tick(0.1)  # limits FPS to 60
            # pygame.time.delay(1000)
            # pygame.display.flip()

        pygame.display.flip()
    # print_area(area)

    cubes_outside = 0
    points = [[0, 0]]

    with tqdm(total=n * n) as pbar:
        while points:
            point = points.pop()

            if area[point[0]][point[1]] == ".":
                area[point[0]][point[1]] = "O"
                cubes_outside += 1
                pbar.update(1)

                draw_pixel(pxarray, point[0], point[1], GREEN)

                for direction in [
                    (-1, -1),
                    (-1, 0),
                    (-1, 1),
                    (0, -1),
                    (0, 1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                ]:
                    new_point = [point[0] + direction[0], point[1] + direction[1]]
                    if (
                        0 <= new_point[0] < n
                        and 0 <= new_point[1] < n
                        and area[new_point[0]][new_point[1]] == "."
                    ):
                        points.append(new_point)

    print(f"{cubes_outside=}")
    result = n * n - cubes_outside
    return result


def main():
    text = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
    # text = input_data_file.read_text()
    result = algo(text)
    print(f"{result=}")


if __name__ == "__main__":
    main()
