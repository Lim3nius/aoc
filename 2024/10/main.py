import argparse
from typing import Any
from collections import namedtuple

Point = namedtuple("Point", ["row", "col"])
Matrix = list[list[int]]


def within_matrix(p: Point, map_: Matrix) -> bool:
    return 0 <= p.row < len(map_) and 0 <= p.col < len(map_[0])


def print_matrix(map_: Matrix):
    for r in map_:
        print("".join([str(c) if c != 0 else "#" for c in r]))


def print_path(map_: Matrix, path: list[Point]):
    for r in range(len(map_)):
        for c in range(len(map_[r])):
            if Point(r, c) in path:
                print("X", end="")
            else:
                print(str(map_[r][c]), end="")
        print()


def find_paths(start: Point, map_: Matrix) -> list[list[Point]]:
    def find_the_9(from_: Point, path: list[Point]) -> list[list[Point]] | None:
        height = map_[from_.row][from_.col]
        if height == 9:
            return [path]

        next_steps = []
        solutions: list[list[Point]] = []

        for dir_ in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = Point(from_.row + dir_[0], from_.col + dir_[1])
            if not within_matrix(next_pos, map_):
                continue

            if map_[next_pos.row][next_pos.col] - height != 1:
                continue

            next_steps.append(next_pos)

        if not next_steps:
            return None

        else:
            for ns in next_steps:
                p = find_the_9(ns, path + [ns])
                if p:
                    solutions.extend(p)

        return solutions

    paths = find_the_9(start, [start])
    return paths


def part1(data: str) -> Any:
    map_: Matrix = [list(map(int, r)) for r in data.splitlines()]

    starts = [Point(r, c) for r in range(len(map_)) for c in range(len(map_[r])) if map_[r][c] == 0]

    total = 0
    for s in starts:
        p = find_paths(s, map_)

        ends = set(map(lambda x: x[-1], p))
        total += len(ends)

    return total


def part2(data: str) -> Any:
    map_: Matrix = [list(map(int, r)) for r in data.splitlines()]

    starts = [Point(r, c) for r in range(len(map_)) for c in range(len(map_[r])) if map_[r][c] == 0]

    total = 0
    for s in starts:
        p = find_paths(s, map_)
        total += len(p)

    return total


def main():
    parser = argparse.ArgumentParser(description="AoC 2024 Day 10")
    parser.add_argument("input", type=str, help="Path to the input file")
    args = parser.parse_args()

    # Read input file
    with open(args.input, "r") as file:
        data = file.read().strip()

    print(f"part1 -> {part1(data)}")
    print(f"part2 -> {part2(data)}")


if __name__ == "__main__":
    main()
