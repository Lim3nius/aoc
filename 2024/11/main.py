import argparse
from typing import Any
from itertools import count
from collections import defaultdict
from functools import cache


@cache
def evolve(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(rp := str(stone)) % 2 == 0:
        return [int(rp[: len(rp) // 2]), int(rp[len(rp) // 2 :])]
    else:
        return [stone * 2024]


def part1(data: str) -> Any:
    return solve(data, 25)


def solve(data: str, cycles: int) -> int:
    stones: dict[int, int] = defaultdict(int)

    for s in list(map(int, data.split(" "))):
        stones[s] += 1

    for i in range(cycles):
        new_stones: dict[int, int] = defaultdict(int)

        for s, cnt in stones.items():
            ev = evolve(s)

            for e in ev:
                new_stones[e] += cnt

        stones = new_stones

    return sum(stones.values())


def part2(data: str) -> Any:
    return solve(data, 75)


def test_input(data: str) -> Any:
    return solve(data, 6)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file")
    parser.add_argument("--test", action="store_true", help="example")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = f.read().strip()

    if args.test:
        print(f"test -> {test_input(data)}")
    else:
        print(f"part1 -> {part1(data)}")
        print(f"part2 -> {part2(data)}")
