from __future__ import annotations
import argparse
from typing import Any
from dataclasses import dataclass


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


UP = vec2(row=-1, col=0)
DOWN = vec2(row=1, col=0)
LEFT = vec2(row=0, col=-1)
RIGHT = vec2(row=0, col=1)

Matrix = list[list[str]]


def move_on_grid(start: vec2, move: str, mat: Matrix) -> tuple[vec2, bool]:
    dir_: vec2 = move_to_dir(move)
    np = start + dir_

    if mat[np.row][np.col] == "#":
        return start, False

    if mat[np.row][np.col] == ".":
        mat[start.row][start.col] = "."
        mat[np.row][np.col] = "@"
        return np, True

    if mat[np.row][np.col] == "O":
        _, moved = move_box1(start=np, move=move, mat=mat)
        if moved:
            mat[start.row][start.col] = "."
            mat[np.row][np.col] = "@"
            return np, True
        return start, False

    raise Exception("wtf?")


def move_box1(start: vec2, move: str, mat: Matrix) -> tuple[vec2, bool]:
    dir_: vec2 = move_to_dir(move)
    np = start + dir_

    if mat[np.row][np.col] == "#":
        return start, False

    if mat[np.row][np.col] == ".":
        mat[start.row][start.col] = "."
        mat[np.row][np.col] = "O"
        return np, True

    if mat[np.row][np.col] == "O":
        _, moved = move_box1(start=np, move=move, mat=mat)
        if moved:
            mat[start.row][start.col] = "."
            mat[np.row][np.col] = "O"
            return np, True
        return start, False

    raise Exception("wtf?")


def move_to_dir(move: str) -> vec2:
    match move:
        case "^":
            return UP
        case ">":
            return RIGHT
        case "<":
            return LEFT
        case "v":
            return DOWN
        case _:
            raise ValueError(f"Invalid move: {move}")


def move_on_grid2(start: vec2, move: str, mat: Matrix) -> tuple[vec2, bool]:
    dir_: vec2 = move_to_dir(move)
    np = start + dir_

    if mat[np.row][np.col] == "#":
        return start, False

    if mat[np.row][np.col] == ".":
        mat[start.row][start.col] = "."
        mat[np.row][np.col] = "@"
        return np, True

    if mat[np.row][np.col] in ["[", "]"]:
        if can_move_box(start=np, move=move, mat=mat):
            move_box2(start=np, move=move, mat=mat)

            mat[start.row][start.col] = "."
            mat[np.row][np.col] = "@"
            return np, True
        return start, False

    raise Exception("wtf?")


def can_move_box(start: vec2, move: str, mat: Matrix) -> bool:
    # print(f"Checking: {start} -> {move}")
    dir_: vec2 = move_to_dir(move)
    left_br = vec2(row=start.row, col=start.col if mat[start.row][start.col] == "[" else start.col - 1)
    np_left_br = left_br + dir_

    if dir_ in [LEFT, RIGHT]:
        if mat[np_left_br.row][np_left_br.col] == "#":
            return False
        elif mat[np_left_br.row][np_left_br.col] == ".":
            return True
        elif mat[np_left_br.row][np_left_br.col] in ["[", "]"]:
            return can_move_box(start=np_left_br + dir_, move=move, mat=mat)
        elif mat[np_left_br.row][np_left_br.col] == "[":
            return can_move_box(start=np_left_br + dir_, move=move, mat=mat)

    space_in_dir = "".join(mat[np_left_br.row][np_left_br.col : np_left_br.col + 2])
    # print(f'Space in dir: "{space_in_dir}"')
    if "#" in space_in_dir:
        return False

    if space_in_dir == "..":
        return True

    if space_in_dir == "[]":
        moved = can_move_box(start=np_left_br, move=move, mat=mat)
        if moved:
            return True
        return False

    if space_in_dir == ".[":
        return can_move_box(start=np_left_br + vec2(0, 1), move=move, mat=mat)

    if space_in_dir == "].":
        return can_move_box(start=np_left_br + vec2(0, -1), move=move, mat=mat)

    if space_in_dir == "][":
        return can_move_box(start=np_left_br + vec2(0, -1), move=move, mat=mat) and can_move_box(
            start=np_left_br + vec2(0, 1), move=move, mat=mat
        )

    raise Exception(f"unexpected case: {space_in_dir}")


def move_box2(start: vec2, move: str, mat: Matrix):
    dir_: vec2 = move_to_dir(move)
    left_br = vec2(row=start.row, col=start.col if mat[start.row][start.col] == "[" else start.col - 1)
    np_left_br = left_br + dir_

    # breakpoint()

    def update(left_br, np_left_br):
        mat[left_br.row][left_br.col] = "."
        mat[left_br.row][left_br.col + 1] = "."
        mat[np_left_br.row][np_left_br.col] = "["
        mat[np_left_br.row][np_left_br.col + 1] = "]"

    # breakpoint()

    if dir_ == LEFT:
        if mat[np_left_br.row][np_left_br.col] == ".":
            update(left_br, np_left_br)
        elif mat[np_left_br.row][np_left_br.col] == "]":
            move_box2(start=np_left_br, move=move, mat=mat)
            update(left_br, np_left_br)
        else:
            breakpoint()
            raise Exception("unexpected case: for move in LEFT or RIGHT")
        return

    if dir_ == RIGHT:
        if mat[np_left_br.row][np_left_br.col + 1] == ".":
            update(left_br, np_left_br)
        elif mat[np_left_br.row][np_left_br.col + 1] == "[":
            move_box2(start=np_left_br + dir_, move=move, mat=mat)
            update(left_br, np_left_br)
        else:
            breakpoint()
            raise Exception("unexpected case: for move in LEFT or RIGHT")
        return

        # if mat[np_left_br.row][np_left_br.col] == ".":
        #     update(left_br, np_left_br)
        # elif mat[np_left_br.row][np_left_br.col] in ["[", "]"]:
        #     move_box2(start=np_left_br, move=move, mat=mat)
        #     update(left_br, np_left_br - dir_)
        # else:
        #     breakpoint()
        #     raise Exception("unexpected case: for move in LEFT or RIGHT")

        # return

    space_in_dir = "".join(mat[np_left_br.row][np_left_br.col : np_left_br.col + 2])
    match space_in_dir:
        case "..":
            update(left_br, np_left_br)

        case "[]":
            move_box2(start=np_left_br, move=move, mat=mat)
            update(left_br, np_left_br)

        case ".[":
            move_box2(start=np_left_br + vec2(0, 1), move=move, mat=mat)
            update(left_br, np_left_br)

        case "].":
            move_box2(start=np_left_br + vec2(0, -1), move=move, mat=mat)
            update(left_br, np_left_br)

        case "][":
            move_box2(start=np_left_br + vec2(0, -1), move=move, mat=mat)
            move_box2(start=np_left_br + vec2(0, 1), move=move, mat=mat)
            update(left_br, np_left_br)

        case _:
            raise Exception(f"unexpected case: {space_in_dir}")


def print_matrix(mat: Matrix):
    for row in mat:
        print("".join(row))


def gps(pos: vec2) -> int:
    return pos.row * 100 + pos.col


def parse_data(input: str) -> tuple[Matrix, str, vec2]:
    mat, moves = input.split("\n\n")

    parsed_matrix = [list(row) for row in mat.splitlines()]

    for rowi in range(len(parsed_matrix)):
        if "@" in parsed_matrix[rowi]:
            start = vec2(row=rowi, col=parsed_matrix[rowi].index("@"))
            break

    pmoves = "".join(moves.splitlines())
    return parsed_matrix, pmoves, start


def matrix2(mat: Matrix) -> Matrix:
    new_mat = []

    for r in mat:
        new_row = []
        for c in r:
            match c:
                case ".":
                    new_row.extend([".", "."])
                case "O":
                    new_row.extend(["[", "]"])
                case "#":
                    new_row.extend(["#", "#"])
                case "@":
                    new_row.extend(["@", "."])

        new_mat.append(new_row)

    return new_mat


def part1(input: str) -> Any:
    matrix, moves, start = parse_data(input)

    for m in moves:
        start, moved = move_on_grid(start, m, matrix)
        # print_matrix(matrix)

    sm = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "O":
                sm += gps(vec2(row=i, col=j))

    return sm


def part2(input_: str) -> Any:
    matrix, moves, start = parse_data(input_)
    matrix = matrix2(matrix)

    for r in range(len(matrix)):
        for i in range(len(matrix[r])):
            if matrix[r][i] == "@":
                start = vec2(row=r, col=i)
                break

    # print_matrix(matrix)

    for m in moves:
        # print(f"Move: {m}")
        start, moved = move_on_grid2(start, m, matrix)
        # print_matrix(matrix)
        # res = input()
        # if res == "br":
        #     breakpoint()

    sm = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "[":
                sm += gps(vec2(row=i, col=j))
    return sm


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file")
    args = parser.parse_args()

    with open(args.input) as f:
        input_ = f.read().strip()

    print(f"Part1 -> {part1(input_)}")
    print(f"Part2 -> {part2(input_)}")
