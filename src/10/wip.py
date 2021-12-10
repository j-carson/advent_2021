from collections import namedtuple
from pathlib import Path

import numpy as np
from ycecream import y as ic

TEST_INPUT = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
TEST_1_SOLUTION = 26397
TEST_2_SOLUTION = 288957


left2right = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def is_left(char):
    return char in left2right.keys()


def is_right(char):
    return char in left2right.values()


def match_brackets(line):
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    match_list = []

    for char in line:
        if is_left(char):
            match_list.append(left2right[char])
        else:
            if (len(match_list) == 0) or (match_list[-1] != char):
                ic(match_list[-1])
                return ic(scores[char])
            else:
                match_list.pop()
    return 0


def complete_brackets(line):
    scores = {")": 1, "]": 2, "}": 3, ">": 4}
    match_list = []

    for char in line:
        if is_left(char):
            match_list.append(left2right[char])
        else:
            if (len(match_list) == 0) or (match_list[-1] != char):
                return 0
            else:
                match_list.pop()

    score = 0
    for char in reversed(match_list):
        score *= 5
        score += scores[char]

    return score


def solve1(lines):
    scores = [match_brackets(line) for line in lines]
    ic(scores)
    return np.sum(scores)


def solve2(lines):
    scores = [complete_brackets(line) for line in lines]
    return np.median([s for s in scores if s != 0])


def parsetext(text):
    lines = text.splitlines()
    return ic(lines)


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
