from functools import cache


@cache
def func0(z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + 12) == INPUT) == 0),
        INPUT,
        (z * ((25 * int(int(((z % 26) + 12) == INPUT) == 0)) + 1)),
    )


@cache
def func1(x, y, z):
    return ((y + 7) * x), (z + ((y + 7) * x))


@cache
def func2(z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + 11) == INPUT) == 0),
        INPUT,
        (z * ((25 * int(int(((z % 26) + 11) == INPUT) == 0)) + 1)),
    )


@cache
def func3(x, y, z):
    return ((y + 15) * x), (z + ((y + 15) * x))


@cache
def func4(x, y, z):
    return ((y + 2) * x), (z + ((y + 2) * x))


@cache
def func5(z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -3) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -3) == INPUT) == 0)) + 1)),
    )


@cache
def func6(z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + 10) == INPUT) == 0),
        INPUT,
        (z * ((25 * int(int(((z % 26) + 10) == INPUT) == 0)) + 1)),
    )


@cache
def func7(x, y, z):
    return ((y + 14) * x), (z + ((y + 14) * x))


@cache
def func8(z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -9) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -9) == INPUT) == 0)) + 1)),
    )


@cache
def func9(z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -7) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -7) == INPUT) == 0)) + 1)),
    )


@cache
def func10(x, y, z):
    return ((y + 1) * x), (z + ((y + 1) * x))


@cache
def func11(z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -11) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -11) == INPUT) == 0)) + 1)),
    )


@cache
def func12(z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -4) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -4) == INPUT) == 0)) + 1)),
    )


@cache
def func13(z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + 14) == INPUT) == 0),
        INPUT,
        (z * ((25 * int(int(((z % 26) + 14) == INPUT) == 0)) + 1)),
    )


@cache
def func14(x, y, z):
    return ((y + 12) * x), (z + ((y + 12) * x))


@cache
def func15(z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -8) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -8) == INPUT) == 0)) + 1)),
    )


@cache
def func16(x, y, z):
    return ((y + 13) * x), (z + ((y + 13) * x))


@cache
def func17(z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -10) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -10) == INPUT) == 0)) + 1)),
    )


def eval_license(INPUTS):
    w = x = y = z = 0
    INPUT = INPUTS[0]
    w, x, y, z = func0(z, INPUT)
    y, z = func1(x, y, z)
    INPUT = INPUTS[1]
    w, x, y, z = func2(z, INPUT)
    y, z = func3(x, y, z)
    INPUT = INPUTS[2]
    w, x, y, z = func0(z, INPUT)
    y, z = func4(x, y, z)
    INPUT = INPUTS[3]
    w, x, y, z = func5(z, INPUT)
    y, z = func3(x, y, z)
    INPUT = INPUTS[4]
    w, x, y, z = func6(z, INPUT)
    y, z = func7(x, y, z)
    INPUT = INPUTS[5]
    w, x, y, z = func8(z, INPUT)
    y, z = func4(x, y, z)
    INPUT = INPUTS[6]
    w, x, y, z = func6(z, INPUT)
    y, z = func3(x, y, z)
    INPUT = INPUTS[7]
    w, x, y, z = func9(z, INPUT)
    y, z = func10(x, y, z)
    INPUT = INPUTS[8]
    w, x, y, z = func11(z, INPUT)
    y, z = func3(x, y, z)
    INPUT = INPUTS[9]
    w, x, y, z = func12(z, INPUT)
    y, z = func3(x, y, z)
    INPUT = INPUTS[10]
    w, x, y, z = func13(z, INPUT)
    y, z = func14(x, y, z)
    INPUT = INPUTS[11]
    w, x, y, z = func2(z, INPUT)
    y, z = func4(x, y, z)
    INPUT = INPUTS[12]
    w, x, y, z = func15(z, INPUT)
    y, z = func16(x, y, z)
    INPUT = INPUTS[13]
    w, x, y, z = func17(z, INPUT)
    y, z = func16(x, y, z)
    return z == 0
