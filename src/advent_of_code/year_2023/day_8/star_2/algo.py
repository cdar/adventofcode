"""
the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost,
you'd probably just start at every node that ends with A and follow all of the paths at the same
time until they all simultaneously end up at nodes that end with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)

Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each
left/right instruction, use that instruction to simultaneously navigate away from both nodes you're
currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only
some of the nodes you're on end with Z, they act like any other node and you continue as normal.) In
this example, you would proceed as follows:

    Step 0: You are at 11A and 22A.
    Step 1: You choose all of the left paths, leading you to 11B and 22B.
    Step 2: You choose all of the right paths, leading you to 11Z and 22C.
    Step 3: You choose all of the left paths, leading you to 11B and 22Z.
    Step 4: You choose all of the right paths, leading you to 11Z and 22B.
    Step 5: You choose all of the left paths, leading you to 11B and 22C.
    Step 6: You choose all of the right paths, leading you to 11Z and 22Z.

So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only
on nodes that end with Z?
"""

from dataclasses import dataclass
from functools import reduce
from math import lcm
from pathlib import Path

from tqdm import tqdm

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "../star_1/input.txt"


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
    current_nodes = [key for key in input_data.nodes.keys() if key.endswith("A")]
    steps_count = 0
    current_instruction = 0
    instructions_loop = 0

    pbar = tqdm()

    while any(not node.endswith("Z") for node in current_nodes):
        if current_instruction >= len(input_data.instructions):
            instructions_loop += 1
            current_instruction = 0
            pbar.update(1)

        for i_current_node in range(len(current_nodes)):
            steps = input_data.nodes[current_nodes[i_current_node]]
            current_nodes[i_current_node] = steps[
                0 if input_data.instructions[current_instruction] == "L" else 1
            ]

        current_instruction += 1
        steps_count += 1

    pbar.close()

    return steps_count


@dataclass
class GraphNode:
    name: str
    left: "GraphNode"
    right: "GraphNode"


def _build_graph(nodes: dict[str, tuple[str, str]]) -> GraphNode:
    _LEFT = 0
    _RIGHT = 1

    graph_nodes: dict[str, GraphNode] = {}

    for node_name in nodes.keys():
        graph_nodes[node_name] = GraphNode(node_name, None, None)

    for node_name, left_right_tuple in nodes.items():
        node = graph_nodes[node_name]
        node.left = graph_nodes[left_right_tuple[_LEFT]]
        node.right = graph_nodes[left_right_tuple[_RIGHT]]

    return graph_nodes


def alog_test_network_perf(input_data: InputData) -> int:
    graph_nodes: dict[str, GraphNode] = _build_graph(input_data.nodes)

    current_nodes: list[GraphNode] = [
        graph_nodes[key] for key in input_data.nodes.keys() if key.endswith("A")
    ]
    steps_count = 0
    current_instruction = 0
    instructions_loop = 0

    pbar = tqdm()

    while any(not node.name.endswith("Z") for node in current_nodes):
        if current_instruction >= len(input_data.instructions):
            instructions_loop += 1
            current_instruction = 0
            pbar.update(1)

        for i_current_node in range(len(current_nodes)):
            node = current_nodes[i_current_node]
            current_nodes[i_current_node] = (
                node.left
                if input_data.instructions[current_instruction] == "L"
                else node.right
            )

        current_instruction += 1
        steps_count += 1

    pbar.close()

    return steps_count


def algo2(input_data: InputData) -> int:
    current_nodes = [key for key in input_data.nodes.keys() if key.endswith("A")]
    steps_count = 0
    current_instruction = 0
    instructions_loop = 0

    nodes_steps = []

    pbar = tqdm()

    while current_nodes:
        if current_instruction >= len(input_data.instructions):
            instructions_loop += 1
            current_instruction = 0
            pbar.update(1)

        next_current_nodes = []
        for current_node in current_nodes:
            steps = input_data.nodes[current_node]
            next_node = steps[
                0 if input_data.instructions[current_instruction] == "L" else 1
            ]
            if next_node.endswith("Z"):
                nodes_steps.append(steps_count + 1)
            else:
                next_current_nodes.append(next_node)
        current_nodes = next_current_nodes

        current_instruction += 1
        steps_count += 1

    pbar.close()

    print(nodes_steps)

    result = reduce(lcm, nodes_steps)

    return result


def start(intput: str) -> int:
    return algo2(parse(intput))


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
    assert 6 == start(
        """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    )
    print("ok")

    print("fourth... ")
    text = input_data_file.read_text()
    print(start(text))
    print("expected: 9606140307013")


if __name__ == "__main__":
    main()
