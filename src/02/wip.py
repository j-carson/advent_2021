from pathlib import Path

import pandas as pd


def getdata():
    data = pd.read_csv("input.txt", sep=" ", header=None)
    data.columns = ["direction", "amount"]
    return data


def part1():
    data = getdata()
    amounts = data.groupby("direction").sum().T
    z = amounts.eval("(down - up) * forward")
    return z.iat[0]


def part2():
    data = getdata()
    aim = 0
    horiz = 0
    depth = 0
    for row in data.itertuples():
        if row.direction == "up":
            aim -= row.amount
        elif row.direction == "down":
            aim += row.amount
        elif row.direction == "forward":
            horiz += row.amount
            depth += aim * row.amount
    return horiz * depth


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
