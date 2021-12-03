from pathlib import Path

import numpy as np


def tobinary(flags):
    result = 0
    power = 1
    for flag in reversed(flags):
        if flag:
            result += power
        power *= 2
    return result


def parsetext(text):
    lines = text.splitlines()
    result = []
    for item in lines:
        bits = [int(i) for i in item]
        result.append(bits)
    return np.array(result)


test = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


def testcase1():
    data = parsetext(test)
    print("testcase", solve_puzzle1(data))


def testcase2():
    data = parsetext(test)
    print("testcase", solve_puzzle2(data))


def solve_puzzle1(data):
    nrows = data.shape[0]
    n_ones = np.array([sum(i) for i in data.T])
    n_zeros = nrows - n_ones

    is_gamma = [n_one > n_zero for n_one, n_zero in zip(n_ones, n_zeros)]
    is_epsilon = [n_one <= n_zero for n_one, n_zero in zip(n_ones, n_zeros)]

    return tobinary(is_gamma) * tobinary(is_epsilon)


def solve_puzzle2(data):
    orig_data = data

    # oxygen rule
    current_bit = 0
    while data.shape[0] > 1:
        nrows = data.shape[0]
        n_ones = np.array([sum(i) for i in data.T])
        n_zeros = nrows - n_ones

        key = int(n_ones[current_bit] >= n_zeros[current_bit])
        data = np.array([row for row in data if row[current_bit] == key])
        current_bit += 1

    oxygen = tobinary(data[0])

    # carbon dioxide rule
    data = orig_data
    current_bit = 0
    while data.shape[0] > 1:
        nrows = data.shape[0]
        n_ones = np.array([sum(i) for i in data.T])
        n_zeros = nrows - n_ones

        key = int(n_ones[current_bit] < n_zeros[current_bit])
        data = np.array([row for row in data if row[current_bit] == key])
        current_bit += 1

    carbon = tobinary(data[0])

    return oxygen, carbon


def getdata():
    text = Path("input.txt").read_text()
    return parsetext(text)


def part1():
    data = getdata()
    testcase1()
    return solve_puzzle1(data)


def part2():
    testcase2()
    data = getdata()
    tup = solve_puzzle2(data)
    return tup[0] * tup[1]


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
