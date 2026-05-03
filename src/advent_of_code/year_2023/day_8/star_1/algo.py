"""
two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow
the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next left/right instruction in
your input. In this example, start with AAA and go right (R) by choosing the right element of AAA,
CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions,
you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the
whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For
example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
"""

from dataclasses import dataclass
from itertools import cycle
from pathlib import Path

from tqdm import tqdm

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"


@dataclass
class InputData:
    instructions: str
    nodes: dict[str, tuple[str, str]]


def _parse_instruction(line: str) -> tuple[str, str, str]:
    return line[0:3], line[7:10], line[12:15]


def parse(text: str) -> InputData:
    lines = text.splitlines()
    nodes = {}
    for line in lines[2:]:
        node = _parse_instruction(line)
        assert node[0] not in nodes
        nodes[node[0]] = node[1:]
    return InputData(lines[0], nodes)


def algo(input_data: InputData) -> int:
    current_node = "AAA"
    steps_count = 0
    current_instruction = 0
    instructions_loop = 0

    pbar = tqdm()
    visited_cache = set()

    while current_node != "ZZZ":
        if current_instruction >= len(input_data.instructions):
            instructions_loop += 1
            current_instruction = 0
            pbar.update(1)

        assert (current_instruction, current_node) not in visited_cache, (
            instructions_loop,
            current_instruction,
            current_node,
            len(visited_cache),
        )
        visited_cache.add((current_instruction, current_node))

        steps = input_data.nodes[current_node]
        current_node = steps[
            0 if input_data.instructions[current_instruction] == "L" else 1
        ]

        current_instruction += 1
        steps_count += 1

    pbar.close()

    return steps_count


def start(intput: str) -> int:
    return algo(parse(intput))


def main():
    print("first... ")
    assert 2 == start(
        """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
    )
    print("ok")
    print("second... ")
    assert 6 == start(
        """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    )
    print("ok")

    print("third... ")
    text = input_data_file.read_text()
    print(start(text))
    print("expected: 19241")


if __name__ == "__main__":
    main()
