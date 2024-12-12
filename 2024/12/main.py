from __future__ import annotations
import argparse
from typing import Any, Generator
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Point:
    row: int  # y
    col: int  # x

    def __add__(self, other: Point) -> Point:
        return Point(row=self.row + other.row, col=self.col + other.col)

    def within(self, mat: Matrix) -> bool:
        return 0 <= self.row < len(mat) and 0 <= self.col < len(mat[0])


def print_matrix(mat: Matrix):
    for row in mat:
        print("".join(row))


@dataclass
class Group:
    letter: str
    points: set[Point] = field(default_factory=set)

    def group_fence(self) -> int:
        fences = 0

        for p in self.points:
            for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                np = p + Point(row=dir[0], col=dir[1])
                if np not in self.points:
                    fences += 1

        return fences

    def cost(self) -> int:
        return len(self.points) * self.group_fence()

    def to_matrix(self) -> Matrix:
        min_row = min(p.row for p in self.points)
        min_col = min(p.col for p in self.points)
        max_row = max(p.row for p in self.points)
        max_col = max(p.col for p in self.points)

        mat = [["." for _ in range(max_col - min_col + 3)] for _ in range(max_row - min_row + 3)]

        for p in self.points:
            mat[p.row - min_row + 1][p.col - min_col + 1] = self.letter

        return mat

    def group_sides(self) -> int:
        sides = 0

        mat = self.to_matrix()
        # print_matrix(mat)
        # print()

        sides = count_horizontal_sides(mat)
        sides += count_vertical_sides(mat)

        return sides

    def reduced_cost(self) -> int:
        cost = len(self.points) * self.group_sides()
        # print(f"letter: {self.letter}, points: {len(self.points)}, sides: {self.group_sides()}, cost: {cost}")
        return cost


def diff_lists(side1, side2):
    diff = []
    for i in range(len(side1)):
        if side1[i] == side2[i]:
            diff.append(0)
        else:
            if side1[i] < side2[i]:
                diff.append(-1)
            else:
                diff.append(1)
    return diff


def count_horizontal_sides(mat: Matrix) -> int:
    sides = 0

    for i in range(len(mat) - 1):
        diff = diff_lists(mat[i], mat[i + 1])
        # diff = [0 if tup[0] == tup[1] else 1 for tup in zip(mat[i], mat[i + 1])]
        # print(diff)

        squashed = squash_same_values(diff)
        sides += sum(map(abs, squashed))
        # print(f"detected sides: {squashed}")

    # print(f"total horizontal sides: {sides}")

    return sides


def count_vertical_sides(mat: Matrix) -> int:
    sides = 0

    for i in range(len(mat[0]) - 1):
        diff = diff_lists([row[i] for row in mat], [row[i + 1] for row in mat])
        # diff = [0 if tup[0] == tup[1] else 1 for tup in zip([row[i] for row in mat], [row[i + 1] for row in mat])]
        # print("\n".join(map(str, diff)))

        squashed = squash_same_values(diff)
        sides += sum(map(abs, squashed))
        # print(f"detected sides: {squashed}")

    # print(f"total vertical sides: {sides}")

    return sides


def squash_same_values(lst: list[Any]) -> list[Any]:
    squashed = [lst[0]]
    last_val = lst[0]

    for i in range(1, len(lst)):
        if lst[i] == last_val:
            continue
        else:
            squashed.append(lst[i])
            last_val = lst[i]

    return squashed


Matrix = list[list[str]]


def neighbors(p: Point, mat: Matrix) -> Generator[Point]:
    for vec in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        np = p + Point(row=vec[0], col=vec[1])
        if np.within(mat):
            yield np


def find_groups(mat: Matrix) -> list[Group]:
    groups: list[Group] = []
    to_search = set([Point(row, col) for row in range(len(mat)) for col in range(len(mat[0]))])

    def bfs_group(pt: Point):
        group = Group(letter=mat[pt.row][pt.col], points={pt})
        others = set()
        to_search = set([pt])

        while to_search:
            pivot = to_search.pop()
            for n in neighbors(pivot, mat):
                if n in others or n in group.points:
                    continue

                if mat[n.row][n.col] == group.letter:
                    group.points.add(n)
                    to_search.add(n)
                else:
                    others.add(n)

        return group, others

    while to_search:
        check = to_search.pop()
        # print(f"len: {len(to_search)}, searching: {to_search}")
        grp, others = bfs_group(check)
        # print(f"found group: {grp.letter}, size: {len(grp.points)}, others: {len(others)}")
        groups.append(grp)
        to_search.difference_update(grp.points)

        # print(f"group: {grp.letter}, size: {len(grp.points)}, fence: {grp.group_fence()}")

    return groups


def part1(data: str) -> Any:
    mat_ = [list(l) for l in data.splitlines()]

    groups = find_groups(mat_)

    return sum(g.cost() for g in groups)


def part2(data: str) -> Any:
    mat_ = [list(l) for l in data.splitlines()]

    groups = find_groups(mat_)

    return sum(g.reduced_cost() for g in groups)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = f.read().strip()

    print(f"part 1 -> {part1(data)}")
    print(f"part 2 -> {part2(data)}")
