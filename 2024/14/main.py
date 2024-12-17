import argparse
from typing import Any
import re
from dataclasses import dataclass
from math import prod


@dataclass
class mvec2:
    row: int
    col: int

    def __str__(self):
        return f"({self.row}, {self.col})"


@dataclass
class PointAndVec:
    point: mvec2
    vec: mvec2

    def step(self, dimensions: mvec2):
        op = mvec2(row=self.point.row, col=self.point.col)
        self.point.row = (self.point.row + self.vec.row) % dimensions.row
        self.point.col = (self.point.col + self.vec.col) % dimensions.col
        # print(f"{op} -> {self.point}")


def parse_coords(input: str) -> mvec2:
    nums = re.findall(r"-?\d+", input)
    return mvec2(col=int(nums[0]), row=int(nums[1]))


def print_matrix(mat: list[list[str]]):
    for row in mat:
        print("".join(row))


def plot_points(data: list[PointAndVec], dimensions: mvec2) -> list[list[str]]:
    mat = [["." for _ in range(dimensions.col)] for _ in range(dimensions.row)]

    for pav in data:
        mat[pav.point.row][pav.point.col] = "#"

    return mat


def q(start: mvec2, end: mvec2, mat: list[PointAndVec]):
    cnt = 0
    for rob in mat:
        if start.row <= rob.point.row < end.row and start.col <= rob.point.col < end.col:
            cnt += 1

    return cnt


def quadrants(data: list[PointAndVec], dimensions: mvec2):
    mat = plot_points(data, dimensions)

    middle_row = dimensions.row // 2
    middle_col = dimensions.col // 2

    print(f"{dimensions}, {middle_row}, {middle_col}")

    mat[middle_row] = ["o" for _ in range(dimensions.col)]
    for i in range(dimensions.row):
        mat[i][middle_col] = "o"

    print_matrix(mat)

    q1 = q(mvec2(row=0, col=0), mvec2(row=middle_row, col=middle_col), data)
    q2 = q(mvec2(row=0, col=middle_col + 1), mvec2(row=middle_row, col=dimensions.col), data)
    q3 = q(mvec2(row=middle_row + 1, col=0), mvec2(row=dimensions.row, col=middle_col), data)
    q4 = q(mvec2(row=middle_row + 1, col=middle_col + 1), mvec2(row=dimensions.row, col=dimensions.col), data)

    print(f"{q1}, {q2}, {q3}, {q4}")
    return prod([q1, q2, q3, q4])


def part1(input: str, test: bool) -> Any:
    dimensions = mvec2(row=103, col=101)
    if test:
        dimensions = mvec2(row=7, col=11)

    data: list[PointAndVec] = []
    for ln in input.splitlines():
        p, v = ln.split(" ")

        pav = PointAndVec(point=parse_coords(p), vec=parse_coords(v))
        data.append(pav)

    # if True:
    #     data = [PointAndVec(point=mvec2(col=2, row=4), vec=mvec2(col=2, row=-3))]

    #     for _ in range(5):
    #         for pav in data:
    #             pav.step(dimensions)
    #         mat = plot_points(data, dimensions)
    #         print_matrix(mat)

    for s in range(100):
        for pav in data:
            pav.step(dimensions)

    return quadrants(data, dimensions)

    # middle_row = round(dimensions.row / 2)
    # middle_col = round(dimensions.col / 2)

    # print(f"{middle_row=}, {middle_col=}")


def part2(input: str) -> Any:
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    with open(args.input) as f:
        input = f.read().strip()

    print(f"Part1 -> {part1(input, args.test)}")
    print(f"Part2 -> {part2(input)}")
