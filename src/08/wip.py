from itertools import permutations
from pathlib import Path

import numpy as np
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


def solve1(data):
    total = 0
    for signal, display in data:
        lengths = [len(d) for d in display]
        flags = [(length in [2, 3, 4, 7]) for length in lengths]
        count = sum(flags)
        total += count
    return total


def transform(signal, mapping):
    xform = "".join(sorted(signal.translate(signal.maketrans(mapping))))
    return xform


def try_translate(signals, mapping):
    for s in signals:
        xform = transform(s, mapping)
        if xform not in signal_to_digit.keys():
            return False
    return True


def brute_force(signals, displays):
    """try every possible mapping of the letters a-g to the letters a-g
    until it matches a set of valid digit codes
    """
    for val in permutations("abcdefg"):
        xlate = {key: value for key, value in zip("abcdefg", val)}
        if try_translate(signals, xlate):
            value = int(
                "".join([signal_to_digit[transform(d, xlate)] for d in displays])
            )
            return value


def solve2(data):
    total = 0
    for signal, display in data:
        total += brute_force(signal, display)
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
