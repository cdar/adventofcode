from array import array
from pathlib import Path

from PIL import Image
from tqdm import tqdm

from commons import get_memory_usage
from year_2023.day_18.star_1_00_pygame_failure.algo import Plan, parse, print_area

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0


def find_min_max_left_right_etc(plan: Plan) -> dict[str, int]:
    maxes = {l: 0 for l in "lrud"}
    current = [0, 0]
    for direction, length in plan:
        match direction:
            case "l":
                current[1] -= length
                maxes[direction] = min(current[1], maxes[direction])
            case "r":
                current[1] += length
                maxes[direction] = max(current[1], maxes[direction])
            case "u":
                current[0] -= length
                maxes[direction] = min(current[0], maxes[direction])
            case "d":
                current[0] += length
                maxes[direction] = max(current[0], maxes[direction])
    return maxes


def get_area_size(maxes: dict[str, int]) -> tuple[int, int]:
    return abs(maxes["u"]) + maxes["d"] + 1, abs(maxes["l"]) + maxes["r"] + 1


def get_start_point(maxes: dict[str, int]) -> tuple[int, int]:
    return abs(maxes["u"]), abs(maxes["l"])


def algo(text: str) -> int:
    plan = parse(text)
    maxes = find_min_max_left_right_etc(plan)
    print(f"{maxes=}")

    y_x = get_area_size(maxes)
    # adding extra 2 for each axis, needed for coloring below
    y_x = y_x[0] + 2, y_x[1] + 2
    print(f"{y_x=}")

    start = get_start_point(maxes)
    # adding extra 1,1
    start = start[0] + 1, start[1] + 1
    print(f"{start=}")

    area = [["."] * y_x[1] for _ in range(y_x[0])]
    y, x = start[0], start[1]

    image = Image.new(mode="RGB", size=(y_x[1], y_x[0]), color=BLACK)

    def draw_pixel(y, x, color=WHITE):
        # print(y, x)
        image.putpixel((x, y), color)

    area[y][x] = "#"
    draw_pixel(y, x)

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
            draw_pixel(y, x)

    image.save("plan.png")
    print_area(area)

    # end of printing/drawing

    cubes_outside = 0
    start = [0, 0]

    # array implementation
    # points = array("H", start)
    # array_length = 2
    # list implementation
    points = [start]

    with tqdm(total=y_x[0] * y_x[1]) as pbar:
        # array implementation
        # while array_length:
        # list implementation
        while points:
            # array implementation
            # point = points.pop(), points.pop()
            # point = point[1], point[0]
            # array_length -= 2
            # list implementation
            point = points.pop()

            if area[point[0]][point[1]] == ".":
                area[point[0]][point[1]] = "O"
                cubes_outside += 1
                pbar.update(1)

                draw_pixel(point[0], point[1], GREEN)

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
                        0 <= new_point[0] < y_x[0]
                        and 0 <= new_point[1] < y_x[1]
                        and area[new_point[0]][new_point[1]] == "."
                    ):
                        # array implementation
                        # points.insert(array_length, new_point[0])
                        # points.insert(array_length + 1, new_point[1])
                        # array_length += 2
                        # list implementation
                        points.append(new_point)

    image.save("plan_colored.png")
    print_area(area)

    print(f"{cubes_outside=}")
    result = y_x[0] * y_x[1] - cubes_outside
    print(f"{get_memory_usage()=}")
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
    text = input_data_file.read_text()
    result = algo(text)
    print(f"{result=}")


if __name__ == "__main__":
    main()
