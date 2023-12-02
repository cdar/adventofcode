"""
As you walk, the Elf shows you a small bag and some cubes which are either red, green,
or blue. Each time you play this game, he will hide a secret number of cubes of each
color in the bag, and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the
bag, grab a handful of random cubes, show them to you, and then put them back in the
bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input).
Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a
semicolon-separated list of subsets of cubes that were revealed from the bag (like 3
red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

In game 1, three sets of cubes are revealed from the bag (and then put back again). The
first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes,
and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag
contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been
loaded with that configuration. However, game 3 would have been impossible because at
one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have
been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs
of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12
red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
"""
from pathlib import Path

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"


def parse_line(line: str) -> tuple[int, list[list[int, int, int]]]:
    game_number, grabs = line.split(":")
    game_number = int(game_number.split(" ")[1])

    result = []
    for grab in grabs.split(";"):
        colors = [0, 0, 0]

        for color in grab.split(","):
            _, number, color = color.split(" ")
            index = ["red", "green", "blue"].index(color)
            colors[index] = int(number)

        result.append(colors)

    return game_number, result


def is_grab_possible(colors: list[int], grab: list[int]) -> bool:
    for c, g in zip(colors, grab):
        if c < g:
            return False
    return True


def algo(colors: list, data: str | list[str]) -> list[int]:
    if isinstance(data, str):
        data = data.splitlines()

    result = []
    for line in data:
        game_number, grabs = parse_line(line)

        for grab in grabs:
            if not is_grab_possible(colors, grab):
                break
        else:
            result.append(game_number)

    return result


if __name__ == "__main__":
    result = algo([12, 13, 14], input_data_file.read_text())
    print(result)
    print("sum:", sum(result))
