from typing import Callable
from operator import add, mul
from functools import reduce

type BinOp = Callable[[int, int], int]


def parseOps(ln: str) -> list[BinOp]:
    opsList: list[BinOp] = []
    for op in ln.split():
        match op:
            case "+":
                opsList.append(add)
            case "*":
                opsList.append(mul)
            case _:
                raise Exception(f"Unexpected value: {op}")
    return opsList


def readInput(file: str) -> tuple[list[list[int]], list[BinOp]]:
    with open(file, "r") as h:
        lns = h.readlines()

    numsLines: list[list[int]] = []
    for ln in lns[:-1]:
        numsLines.append([int(x) for x in ln.split()])

    problems: list[list[int]] = []
    for col in range(0, len(numsLines[0])):
        problems.append([num[col] for num in numsLines])

    opsList = parseOps(lns[-1])

    return problems, opsList


def readCephaloInput(file: str) -> tuple[list[list[int]], list[BinOp]]:
    with open(file, "r") as h:
        lns = h.readlines()

    opsList = parseOps(lns[-1])
    opsList = opsList[::-1]

    cephaloProblems: list[list[int]] = []
    cephaloNums: list[int] = []
    for idx in range(len(lns[0]) - 1, -1, -1):
        ciphers = [ln[idx] for ln in lns[:-1]]
        nm = "".join(ciphers)

        if nm.strip() == "":
            cephaloProblems.append(cephaloNums)
            cephaloNums = []
            continue

        cephaloNums.append(int(nm))
    cephaloProblems.append(cephaloNums)
    cephaloProblems = cephaloProblems[1:]  # discard empty list (last line is full of newlines)

    return cephaloProblems, opsList


def part1(file: str):
    problems, ops = readInput(file)

    total = 0

    for i in range(0, len(problems)):
        num = reduce(ops[i], problems[i])
        total += num

    return total


def part2(file: str):
    problems, ops = readCephaloInput(file)

    total = 0

    for i in range(0, len(problems)):
        num = reduce(ops[i], problems[i])
        total += num

    return total


print(f"Part1 -> {part1('input.txt')}")
print(f"Part2 -> {part2('input.txt')}")
