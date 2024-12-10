import argparse
from typing import Any


def rotate_right(direction: tuple[int, int]) -> tuple[int, int]:
    match direction:
        case (-1, 0):
            return 0, 1
        case (0, 1):
            return 1, 0
        case (1, 0):
            return 0, -1
        case (0, -1):
            return -1, 0

    raise Exception("Invalid direction")


def print_matrix(matrix: list[list[str]]):
    for row in matrix:
        print(row)


def pos_in_matrix(matrix: list[list[str]], pos: tuple[int, int]) -> bool:
    return 0 <= pos[0] < len(matrix) and 0 <= pos[1] < len(matrix[pos[0]])


def move(matrix: list[list[str]], pos: tuple[int, int], direction: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    new_pos = pos[0] + direction[0], pos[1] + direction[1]
    new_dir = direction

    if not pos_in_matrix(matrix, new_pos):
        raise StopIteration

    for _ in range(4):
        if not pos_in_matrix(matrix, new_pos):
            raise StopIteration

        if matrix[new_pos[0]][new_pos[1]] == "#":
            new_dir = rotate_right(new_dir)
            new_pos = pos[0] + new_dir[0], pos[1] + new_dir[1]
        else:
            break
    else:
        breakpoint()
        raise Exception("surrounded by crates")

    return new_pos, new_dir


def process_data(data: str) -> tuple[list[list[str]], tuple[int, int]]:
    matrix = [list(row) for row in data.splitlines()]

    def find_pos():
        for r in range(len(matrix)):
            for c in range(len(matrix[r])):
                if matrix[r][c] == "^":
                    return (r, c)

    pos = find_pos()
    return matrix, pos


def get_visited(matrix: list[list[str]], pos: tuple[int, int], direction: tuple[int, int]) -> list[list[bool]]:
    visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    visited[pos[0]][pos[1]] = True
    while True:
        try:
            pos, direction = move(matrix, pos, direction)
            visited[pos[0]][pos[1]] = True
        except StopIteration:
            break

    return visited


def part1(data: str) -> Any:
    matrix, pos = process_data(data)
    direction = (-1, 0)

    visited = get_visited(matrix, pos, direction)

    # visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    # visited[pos[0]][pos[1]] = True
    # while True:
    #     try:
    #         pos, direction = move(matrix, pos, direction)
    #         visited[pos[0]][pos[1]] = True
    #     except StopIteration:
    #         break

    # for r in visited:
    #     print([int(n) for n in r])

    return sum(sum(1 for v in row if v) for row in visited)
    pass


def will_get_stuck(pos_loc: tuple[int, int], matrix: list[list[str]], pos: tuple[int, int], dir: tuple[int, int]) -> bool:
    matcopy = [list(row) for row in matrix]
    matcopy[pos_loc[0]][pos_loc[1]] = "#"
    moves: set[tuple[tuple[int, int], tuple[int, int]]] = set()

    while True:
        try:
            pos, dir = move(matcopy, pos, dir)
            if (pos, dir) in moves:
                # print(moves)
                return True
            else:
                moves.add((pos, dir))

        except StopIteration:
            # print(moves)
            return False

    raise Exception("What the hell?")


def part2(data: str) -> Any:
    matrix, pos = process_data(data)
    direction = (-1, 0)

    visited = get_visited(matrix, pos, direction)

    stuck_pos = []
    for pos_loc in (
        (r, c) for r in range(len(matrix)) for c in range(len(matrix[r])) if matrix[r][c] not in ["#", "^"] and visited[r][c]
    ):
        if will_get_stuck(pos_loc, matrix, pos, direction):
            stuck_pos.append(pos_loc)

    return len(stuck_pos)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="file with input data")
    args = ap.parse_args()

    with open(args.input) as f:
        data = f.read().strip()

    print(f"part1 -> {part1(data)}")
    print(f"part2 -> {part2(data)}")


if __name__ == "__main__":
    main()
