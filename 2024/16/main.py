from __future__ import annotations
import argparse
from typing import Any
from dataclasses import dataclass
import sys

sys.setrecursionlimit(10_000)

Matrix = list[list[str]]


@dataclass
class vec2:
    row: int
    col: int

    def __add__(self, other: vec2):
        return vec2(row=self.row + other.row, col=self.col + other.col)

    def __mul__(self, other: int):
        return vec2(row=self.row * other, col=self.col * other)

    def __sub__(self, other: vec2):
        return vec2(row=self.row - other.row, col=self.col - other.col)


def within_matrix(matrix: Matrix, pos: vec2) -> bool:
    return 0 <= pos.row < len(matrix) and 0 <= pos.col < len(matrix[0])


UP = vec2(row=-1, col=0)
DOWN = vec2(row=1, col=0)
LEFT = vec2(row=0, col=-1)
RIGHT = vec2(row=0, col=1)


@dataclass
class Move:
    pos: vec2
    dir_: vec2
    score: int


def parse_map(input: str) -> tuple[Matrix, vec2, vec2]:
    matrix = [list(line) for line in input.split("\n")]
    start = None
    end = None

    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == "S":
                start = vec2(r, c)
            elif matrix[r][c] == "E":
                end = vec2(r, c)

    assert start and end
    return matrix, start, end


def print_matrix(matrix: list[list[int]]):
    for row in matrix:
        for col in row:
            print(f"{col if col != 2**64-1 else -1 :7d}", end="")
        print("\n\n")
    print()


def print_matrix_visited(matrix: Matrix, visited: list[vec2]):
    mat = [r.copy() for r in matrix]

    for v in visited:
        mat[v.row][v.col] = "*"

    for r in mat:
        print("".join(r))


def bfs(matrix: Matrix, start: vec2, end: vec2) -> int:
    reached_pos_lowest_score = [[2**64 - 1 for c in range(len(matrix[r]))] for r in range(len(matrix))]
    reached_pos_lowest_score[start.row][start.col] = 0

    queue = [Move(pos=start, dir_=RIGHT, score=0)]

    while queue:
        mov = queue.pop(0)
        pos = mov.pos
        dir_ = mov.dir_

        for dir_ in [UP, DOWN, LEFT, RIGHT]:
            if dir_ == mov.dir_ * -1:  # no way back
                continue

            score = mov.score
            score += 1 if dir_ == mov.dir_ else 1001

            new_pos = pos + dir_

            if matrix[new_pos.row][new_pos.col] == "#":  # wall
                continue

            if reached_pos_lowest_score[new_pos.row][new_pos.col] < score:
                continue

            reached_pos_lowest_score[new_pos.row][new_pos.col] = score
            queue.append(Move(pos=new_pos, dir_=dir_, score=score))

    print_matrix(reached_pos_lowest_score)
    return reached_pos_lowest_score[end.row][end.col]


def part1(input: str) -> Any:
    mat, start, end = parse_map(input)

    return bfs(mat, start, end)


def part2(input: str) -> Any:
    mat, start, end = parse_map(input)

    # bfs(mat, start, end)
    # bfs(mat, end, start)
    return 42


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file")
    args = parser.parse_args()

    with open(args.input) as f:
        input_ = f.read().strip()

    print(f"Part1 -> {part1(input_)}")
    print(f"Part2 -> {part2(input_)}")
