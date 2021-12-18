from itertools import permutations
from pathlib import Path

from number_class import NumberLeaf, NumberTree
from ycecream import y as ic


def part1():
    lines = Path("input.txt").read_text().splitlines()

    total = NumberTree.from_string(lines[0])
    for line in lines[1:]:
        add_on = NumberTree.from_string(line)
        total += add_on

    print("Part 1", total.magnitude)


def part2():
    lines = Path("input.txt").read_text().splitlines()
    numbers = [NumberTree.from_string(line) for line in lines]
    result = max([(tup[0] + tup[1]).magnitude for tup in permutations(numbers, 2)])

    print("Part 2", result)


if __name__ == "__main__":
    part1()
    part2()
