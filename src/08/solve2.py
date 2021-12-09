# Second solution done a day later using logic rather than brute force

from itertools import accumulate, permutations
from pathlib import Path

import numpy as np
import pandas as pd
from ycecream import y as ic

TEST_INPUT = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

TEST_1_SOLUTION = 26
TEST_2_SOLUTION = 61229

digit_to_signal = {
    "0": "abcefg",
    "1": "cf",  # special
    "2": "acdeg",
    "3": "acdfg",
    "4": "bcdf",  # special
    "5": "abdfg",
    "6": "abdefg",
    "7": "acf",  # special
    "8": "abcdefg",  # special
    "9": "abcdfg",
}
signal_to_digit = {value: key for key, value in digit_to_signal.items()}

ALPHABET = "abcdefg"


def solve1(data):
    total = 0
    for signal, display in data:
        lengths = [len(d) for d in display]
        flags = [(length in [2, 3, 4, 7]) for length in lengths]
        count = sum(flags)
        total += count
    return total


def complementary_letters(word):
    """return the letters in ALPHABET that are not in word"""
    return [c for c in ALPHABET if c not in word]


def transform(word, mapping):
    """change the characters in word to the letters in given dictionary mapping"""
    xform = "".join(sorted(word.translate(word.maketrans(mapping))))
    return xform


class LogicPuzzle:
    """Class to mark X's on boards where mapping from letter-in-row to letter-in-column
    has been eliminated as a solution"""

    def __init__(self):
        self.board = pd.DataFrame(index=list(ALPHABET), columns=list(ALPHABET), data="")

    def is_not(self, rows, cols):
        """the keys in 'rows' do not match to any of the keys in 'cols'"""
        for row in rows:
            for col in cols:
                self.board.loc[row, col] = "X"

    def is_(self, rows, cols):
        self.is_not(rows, complementary_letters(cols))

    def solve(self):
        mapping = {}
        for index, *row in self.board.itertuples():
            for letter, mark in zip(ALPHABET, row):
                if mark != "X":
                    mapping[index] = letter
                    break
        return mapping


def solve2(data):
    total = 0
    for signal, display in data:
        board = LogicPuzzle()
        for s in signal:
            if len(s) == 2:
                board.is_(s, "cf")  # 1
                board.is_not(complementary_letters(s), "cf")
            elif len(s) == 3:
                board.is_(s, "acf")  # 7
                board.is_not(complementary_letters(s), "acf")
            elif len(s) == 4:
                board.is_(s, "bcdf")  # 4
                board.is_not(complementary_letters(s), "bcdf")

        # 2, 3, 5
        length_5 = [set(s) for s in signal if len(s) == 5]
        inters_5 = length_5[0]
        for item in length_5[1:]:
            inters_5 = inters_5 & item
        # the three slots the above numbers have
        # in common are the horizontal bars
        if len(inters_5) == 3:
            board.is_(inters_5, "adg")
            board.is_not(complementary_letters(inters_5), "adg")

        # 0, 6, 9
        length_6 = [set(s) for s in signal if len(s) == 6]
        inters_6 = length_6[0]
        for item in length_6[1:]:
            inters_6 = inters_6 & item
        # the slots the 6 and 9 have in common
        if len(inters_6) == 4:
            board.is_(inters_6, "abfg")
            board.is_not(complementary_letters(inters_6), "abfg")

        xlate = board.solve()
        total += int("".join([signal_to_digit[transform(d, xlate)] for d in display]))

    return total


def parsetext(text):
    result = []
    lines = text.splitlines()

    for line in lines:
        signal, display = line.split("|")
        signals = signal.split()
        displays = display.split()
        result.append((signals, displays))

    return result


def mydata():
    return Path("input.txt").read_text()


def part1():
    # turn on debug print statements
    ic.enabled = True
    result = solve1(parsetext(TEST_INPUT))
    assert result == TEST_1_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve1(parsetext(mydata()))


def part2():

    # turn on debug print statements
    ic.enabled = True
    result = solve2(parsetext(TEST_INPUT))
    assert result == TEST_2_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve2(parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
