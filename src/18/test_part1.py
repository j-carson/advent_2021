import pytest
from number_class import NumberLeaf, NumberTree


@pytest.mark.parametrize(
    "string",
    [
        "[1,2]",
        "[[1,2],3]",
        "[9,[8,7]]",
        "[[1,9],[8,5]]",
        "[[[[1,2],[3,4]],[[5,6],[7,8]]],9]",
        "[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]",
        "[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]",
    ],
)
def test_init(string):
    tree = NumberTree.from_string(string)
    list_ = eval(string)
    assert tree.to_list() == list_


"""
    [[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4] (the 9 has no regular number to its left, so it is not added to any regular number).
    [7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]] (the 2 has no regular number to its right, and so it is not added to any regular number).
    [[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3].
    [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] (the pair [3,2] is unaffected because the pair [7,3] is further to the left; [3,2] would explode on the next action).
    [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[7,0]]]].
"""


@pytest.mark.parametrize(
    "initial,expected_result",
    [
        ([[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4]),
        ([7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]]),
        ([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]),
        (
            [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]],
            [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
        ),
        (
            [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
            [[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
        ),
    ],
)
def test_explode_1(initial, expected_result):
    start = NumberTree.from_list(initial)
    spot = start.can_explode()
    spot.explode()
    result = start.to_list()
    assert result == expected_result


"""
Here is the process of finding the reduced result of [[[[4,3],4],4],[7,[[8,4],9]]] + [1,1]:

after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
after explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
after explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
after explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

"""


def expect_explode(tree):
    assert tree.can_explode() is not None
    return True


def expect_split(tree):
    assert tree.can_explode() is None
    assert tree.can_split() is not None
    return True


def test_long_example():
    result = NumberTree.from_list([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])

    assert expect_explode(result)
    assert result.reduce_iteration()
    assert result.to_list() == [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]

    assert expect_explode(result)
    assert result.reduce_iteration()
    assert result.to_list() == [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]

    assert expect_split(result)
    assert result.reduce_iteration()
    assert result.to_list() == [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]

    assert expect_split(result)
    assert result.reduce_iteration()
    assert result.to_list() == [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]

    assert expect_explode(result)
    assert result.reduce_iteration()
    assert result.to_list() == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]

    assert not result.reduce_iteration()


@pytest.mark.parametrize(
    "sum_,list_",
    (
        (
            [[[[1, 1], [2, 2]], [3, 3]], [4, 4]],
            [
                [1, 1],
                [2, 2],
                [3, 3],
                [4, 4],
            ],
        ),
        (
            [[[[3, 0], [5, 3]], [4, 4]], [5, 5]],
            [
                [1, 1],
                [2, 2],
                [3, 3],
                [4, 4],
                [5, 5],
            ],
        ),
        (
            [[[[5, 0], [7, 4]], [5, 5]], [6, 6]],
            [
                [1, 1],
                [2, 2],
                [3, 3],
                [4, 4],
                [5, 5],
                [6, 6],
            ],
        ),
        (
            [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]],
            [
                [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
                [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
                [[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]],
                [[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]],
                [7, [5, [[3, 8], [1, 4]]]],
                [[2, [2, 2]], [8, [8, 1]]],
                [2, 9],
                [1, [[[9, 3], 9], [[9, 0], [0, 7]]]],
                [[[5, [7, 4]], 7], 1],
                [[[[4, 2], 2], 6], [8, 7]],
            ],
        ),
    ),
)
def test_addition(sum_, list_):
    total = NumberTree.from_list(list_[0])
    for item in list_[1:]:
        total = total + NumberTree.from_list(item)
    assert total.to_list() == sum_


"""
Here are a few more magnitude examples:

    [[1,2],[[3,4],5]] becomes 143.
    [[[[0,7],4],[[7,8],[6,0]]],[8,1]] becomes 1384.
    [[[[1,1],[2,2]],[3,3]],[4,4]] becomes 445.
    [[[[3,0],[5,3]],[4,4]],[5,5]] becomes 791.
    [[[[5,0],[7,4]],[5,5]],[6,6]] becomes 1137.
    [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] becomes 3488.

"""


@pytest.mark.parametrize(
    "number,magnitude",
    (
        ([[1, 2], [[3, 4], 5]], 143),
        ([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]], 1384),
        ([[[[1, 1], [2, 2]], [3, 3]], [4, 4]], 445),
        ([[[[3, 0], [5, 3]], [4, 4]], [5, 5]], 791),
        ([[[[5, 0], [7, 4]], [5, 5]], [6, 6]], 1137),
        ([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]], 3488),
    ),
)
def test_magnitude(number, magnitude):
    tree = NumberTree.from_list(number)
    assert tree.magnitude == magnitude
