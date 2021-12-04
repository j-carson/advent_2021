from pathlib import Path

import numpy as np
from ycecream import y


class Winner(Exception):
    def __init__(self, number_called: int):
        self.num = number_called
        message = f"Bingo! {number_called}"
        super().__init__(message)


class Bingo:
    def __init__(self, text):
        board = []
        lines = text.splitlines()
        for line in lines:
            board.append([int(n) for n in line.split()])

        self.status = np.zeros((5, 5)).astype(int)
        self.numbers = np.array(board)
        self.winner = False

    def play(self, number):
        # same board never raises twice
        if self.winner:
            return
        self.status[self.numbers == number] = 1
        rowsums = [sum(row) for row in self.status]
        colsums = [sum(row) for row in self.status.T]
        if 5 in rowsums or 5 in colsums:
            self.winner = True
            raise Winner(number)


def solve1(numbers, boards):
    for number in numbers:
        for board in boards:
            try:
                board.play(number)
            except Winner:
                board.numbers[board.status == 1] = 0
                unmarked = np.sum(board.numbers.flatten())
                return unmarked * number


def solve2(numbers, boards):
    board_left = len(boards)
    for number in numbers:
        for board in boards:
            try:
                board.play(number)
            except Winner:
                board_left -= 1
                if board_left == 0:
                    board.numbers[board.status == 1] = 0
                    unmarked = np.sum(board.numbers.flatten())
                    return unmarked * number


def parsetext(text):
    chunks = text.split("\n\n")
    numbers = [int(n) for n in chunks[0].split(",")]
    boards = []

    for chunk in chunks[1:]:
        boards.append(Bingo(chunk))

    return numbers, boards


def testdata():
    return """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


def mydata():
    return Path("input.txt").read_text()


def part1():
    test_solution = 4512
    result = solve1(*parsetext(testdata()))
    assert result == test_solution

    return solve1(*parsetext(mydata()))


def part2():
    test_solution = 1924
    result = solve2(*parsetext(testdata()))
    assert result == test_solution

    return solve2(*parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
