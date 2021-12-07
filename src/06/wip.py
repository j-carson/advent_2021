from pathlib import Path

import numpy as np
from ycecream import y as ic

TEST_INPUT = "3,4,3,1,2"
TEST_1_SOLUTION = 5934
TEST_2_SOLUTION = 26984457539


class Clock:
    def __init__(self):
        self.day = -1
        self.items = []
        self.newitems = []

    def tick(self):
        self.day += 1
        for item in self.items:
            item.tick()

        self.items = self.newitems
        self.newitems = []

    def add_item(self, item):
        for newi in self.newitems:
            if item.counter == newi.counter:
                newi.score += item.score
                break
        else:
            self.newitems.append(item)

    def visualize(self):
        ic([f"{c.counter}x{c.score}" for c in self.items], prefix=f"{self.day} ==>")

    def score(self):
        return sum([item.score for item in self.items])


class LanternFish:
    def __init__(self, counter, clock, score=None):
        self.counter = counter
        self.clock = clock
        if score is None:
            self.score = 1
        else:
            self.score = score

    def tick(self):
        self.counter -= 1
        if self.counter < 0:
            self.clock.add_item(LanternFish(6, self.clock, self.score))
            self.clock.add_item(LanternFish(8, self.clock, self.score))
        else:
            self.clock.add_item(LanternFish(self.counter, self.clock, self.score))


def solve1(data, generations=80):

    clock = Clock()

    for counter in data:
        clock.add_item(LanternFish(counter, clock))

    for i in range(generations + 1):
        clock.tick()
        clock.visualize()

    return clock.score()


def solve2(data, generations=256):
    return solve1(data, generations)


def parsetext(text):
    return [int(i) for i in text.split(",")]


def mydata():
    return Path("input.txt").read_text()


def part1():
    # turn on debug print statements
    ic.enabled = False
    result = solve1(parsetext(TEST_INPUT))
    assert result == TEST_1_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve1(parsetext(mydata()))


def part2():

    # turn on debug print statements
    ic.enabled = False
    result = solve2(parsetext(TEST_INPUT))
    assert result == TEST_2_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve2(parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
