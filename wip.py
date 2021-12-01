# Replacement for aoc-cli template

from pathlib import Path


def inputparser():
    text = Path("input.txt").read_text()
    lines = text.splitlines()
    return lines


def part1():
    return 0


def part2():
    return 0


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
