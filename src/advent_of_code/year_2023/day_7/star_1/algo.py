"""
In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of
each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456

Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

    32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
    KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
    T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.

Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.
"""

import typing as t
from collections import defaultdict
from dataclasses import dataclass
from functools import cmp_to_key, reduce
from pathlib import Path

CUR_DIR = Path(__file__).parent.resolve()
input_data_file = CUR_DIR / "input.txt"


CARDS_STRENGTH = dict(reversed(el) for el in enumerate(reversed("AKQJT98765432")))


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


def _calc_hand(hand: str) -> list[int]:
    hand_map = defaultdict(int)
    for card in hand:
        hand_map[card] += 1
    return sorted(hand_map.values(), reverse=True)


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
        calc_items.append((_calc_hand(hand_item.hand), hand_item))

    calc_items.sort(key=cmp_to_key(_hands_cmp))

    result = 0
    for i, item in enumerate(calc_items, 1):
        result += i * item[1].bid

    return result


def start(intput: str) -> int:
    return algo(parse(intput))


def main():
    assert 6440 == start(
        """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    )

    text = input_data_file.read_text()
    print(start(text))
    print("expected: 251545216")


if __name__ == "__main__":
    main()
