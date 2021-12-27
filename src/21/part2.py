from collections import Counter, defaultdict
from functools import cache
from itertools import chain, count, cycle, product
from pathlib import Path

import numpy as np
from ycecream import y as ic

TEST_INPUT = """Player 1 starting position: 4
Player 2 starting position: 8"""
MY_INPUT = """Player 1 starting position: 8
Player 2 starting position: 2"""

TEST_2_SOLUTION = 444356092776315
TEST_2_PLAYER2 = 341960390180808

WINNING_SCORE = 21


class DiracDice:
    __slots__ = [
        "value_counts",
    ]

    def __init__(self, sides, rolls_per_turn):
        self.value_counts = Counter(
            [
                sum(rolls)
                for rolls in product(range(1, sides + 1), repeat=rolls_per_turn)
            ]
        )

    def items(self):
        yield from self.value_counts.items()


@cache
def count_wins(combinations, player1_pos, player1_score, player2_pos, player2_score):

    dice = DiracDice(sides=3, rolls_per_turn=3)
    wins = 0
    losses = 0

    for roll, universes in dice.items():

        new_pos = player1_pos + roll
        if new_pos > 10:
            new_pos -= 10
        new_score = player1_score + new_pos
        new_universes = combinations * universes

        if new_score >= WINNING_SCORE:
            wins += new_universes
        else:
            uwin, ulose = count_wins(
                new_universes, player2_pos, player2_score, new_pos, new_score
            )
            wins += ulose
            losses += uwin

    return (wins, losses)


def parsetext(text):
    positions = []
    lines = text.splitlines()
    for line in lines:
        positions.append(int(line.split(":")[1]))
    return positions


def part2():
    positions = parsetext(TEST_INPUT)
    ic(positions)
    wins, losses = count_wins(1, positions[0], 0, positions[1], 0)
    ic(wins, losses)
    ic(TEST_2_SOLUTION, TEST_2_PLAYER2)
    assert max([wins, losses]) == TEST_2_SOLUTION
    assert min([wins, losses]) == TEST_2_PLAYER2

    # turn off debug print statements
    positions = parsetext(MY_INPUT)
    wins, losses = count_wins(1, positions[0], 0, positions[1], 0)
    return max([wins, losses])


result = part2()
print("Part 2: ", result)
