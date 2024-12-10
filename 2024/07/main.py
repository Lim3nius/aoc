from typing import Any
import argparse
from itertools import product


def process_data(data) -> list[tuple[int, list[int]]]:
    lines = data.splitlines()
    parsed = []
    for ln in lines:
        res, coefs = ln.split(":")
        result = int(res)
        coefs = [int(x) for x in coefs.strip().split(" ")]
        parsed.append((result, coefs))
    return parsed


def find_eq_solution(res: int, coefs: list[int], symbols: list[str]) -> tuple[Any, ...] | None:
    for ops in product(symbols, repeat=len(coefs) - 1):
        acc = coefs[0]
        for i in range(0, len(coefs) - 1):
            if ops[i] == "+":
                acc += coefs[i + 1]
            elif ops[i] == "*":
                acc *= coefs[i + 1]
            elif ops[i] == "||":
                # print(f"new op: {acc} || {coefs[i + 1]} ->", end=" ")
                acc = int(str(acc) + str(coefs[i + 1]))
                # print(acc)
            else:
                raise ValueError(f"Unknown operator {ops[i]}")

        if acc == res:
            return ops

    return None


def part1(data) -> Any:
    equations = process_data(data)

    solvable = []
    for res, coefs in equations:
        if ops := find_eq_solution(res, coefs, symbols=["*", "+"]):
            solvable.append((res, coefs, ops))

    # for s in solvable:
    #     print(s)

    return sum(x[0] for x in solvable)


def part2(data) -> Any:
    equations = process_data(data)

    solvable = []
    for res, coefs in equations:
        if ops := find_eq_solution(res, coefs, symbols=["*", "+", "||"]):
            solvable.append((res, coefs, ops))

    # for s in solvable:
    #     print(s)

    return sum(x[0] for x in solvable)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="file with input data")
    args = ap.parse_args()

    with open(args.input) as f:
        data = f.read().strip()

    print(f"part1 -> {part1(data)}")
    print(f"part2 -> {part2(data)}")
