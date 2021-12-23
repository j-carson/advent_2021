from itertools import count, cycle

from ycecream import y as ic

TEST_INPUT = """Player 1 starting position: 4
Player 2 starting position: 8"""
MY_INPUT = """Player 1 starting position: 8
Player 2 starting position: 2"""

TEST_1_SOLUTION = 739785


class DeterministicDice:
    __slots__ = ["n_rolls"]

    def __init__(self):
        self.n_rolls = 0

    def roll(self):
        for j in count(1):
            self.n_rolls += 3
            yield 3 * (3 * j - 1)


class Player:
    __slots__ = ["name", "pos", "score"]

    def __init__(self, name, starting_pos):
        self.name = name
        self.pos = starting_pos
        self.score = 0

    def play(self, roll):
        self.pos += roll % 10
        if self.pos > 10:
            self.pos -= 10
        self.score += self.pos

    @property
    def winner(self):
        return self.score >= 1000


def playgame(player1_start, player2_start):

    ic(player1_start, player2_start)

    player1, player2 = Player(1, player1_start), Player(2, player2_start)
    turn_keeper = cycle([player1, player2])
    die = DeterministicDice()
    roller = die.roll()

    for n_turns, roll, player in zip(count(1), roller, turn_keeper):
        player.play(roll)

        # Print debug stuff for first few and last few turns
        # of test case
        if n_turns < 20:
            ic(player.name, roll, player.pos, player.score)

        if player2.score > 740:
            ic(player.name, roll, player.pos, player.score)

        if player.winner:
            other_player = next(turn_keeper)
            return ic(other_player.score * die.n_rolls)


def parsetext(text):
    positions = []
    lines = text.splitlines()
    for line in lines:
        positions.append(int(line.split(":")[1]))
    return positions


def part1():
    # turn on debug print statements
    ic.enabled = False
    result = playgame(*parsetext(TEST_INPUT))
    assert result == TEST_1_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return playgame(*parsetext(MY_INPUT))


result = part1()
print("Part 1: ", result)
