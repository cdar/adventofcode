"""
--- Part Two ---

To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

    32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
    KK677 is now the only two pair, making it the second-weakest hand.
    T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.

With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
"""

import typing as t
from collections import defaultdict
from dataclasses import dataclass
from functools import cmp_to_key
from pathlib import Path

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "../star_1/input.txt"


CARDS_STRENGTH = dict(reversed(el) for el in enumerate(reversed("AKQT98765432J")))


@dataclass
class HandItem:
    hand: str
    bid: int


def parse(text: str) -> list[HandItem]:
    result = []
    for line in text.splitlines():
        hand, bid = line.split()
        bid = int(bid)
        result.append(HandItem(hand, bid))
    return result


def strcmp(a: t.Any, b: t.Any) -> int:
    return (a > b) - (a < b)


def apply_joker_logic(hand_map: dict[str, int]) -> list[int]:
    j_cards = hand_map.pop("J", None)
    result = sorted(hand_map.values(), reverse=True)

    if j_cards is None:
        return result

    if result:
        result[0] += j_cards
    else:
        result = [j_cards]
    return result


def calculate_hand_strangth(hand: str) -> list[int]:
    hand_map = defaultdict(int)
    for card in hand:
        hand_map[card] += 1
    return apply_joker_logic(hand_map)


def _hands_cmp(a: tuple[list[int], HandItem], b: tuple[list[int], HandItem]) -> int:
    result = strcmp(a[0], b[0])
    if result != 0:
        return result

    for i in range(5):
        result = CARDS_STRENGTH[a[1].hand[i]] - CARDS_STRENGTH[b[1].hand[i]]
        if result != 0:
            break

    return result


def algo(items: list[HandItem]) -> int:
    calc_items: tuple[list[int], HandItem] = []
    for hand_item in items:
        calc_items.append((calculate_hand_strangth(hand_item.hand), hand_item))

    calc_items.sort(key=cmp_to_key(_hands_cmp))

    result = 0
    for i, item in enumerate(calc_items, 1):
        result += i * item[1].bid

    return result


def start(intput: str) -> int:
    return algo(parse(intput))


def main():
    assert 5905 == start(
        """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    )

    text = input_data_file.read_text()
    print(start(text))
    print("expected: 250384185")


if __name__ == "__main__":
    main()
