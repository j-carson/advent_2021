from pathlib import Path


def solve1(data):
    return 0


def solve2(data):
    return 0


def parsetext(text):
    lines = text.splitlines()
    return lines


def testdata():
    return ""


def mydata():
    return Path("input.txt").read_text()


def part1():
    test_solution = 0
    result = solve1(parsetext(testdata()))
    assert result == test_solution

    return solve1(parsetext(mydata()))


def part2():
    test_solution = 0
    result = solve2(parsetext(testdata()))
    assert result == test_solution

    return solve2(parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
