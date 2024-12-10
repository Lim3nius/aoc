import argparse
from typing import Any


def directions(row, col) -> list[list[tuple[int, int]]]:
    indices = []
    for vec in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        indices.append(
            [
                (row, col),
                (row + vec[0], col + vec[1]),
                (row + 2 * vec[0], col + 2 * vec[1]),
                (row + 3 * vec[0], col + 3 * vec[1]),
            ]
        )

    return indices


def mas_directions(row: int, col: int) -> list[tuple[int, int]]:
    return [
        (row - 1, col - 1),
        (row, col),
        (row + 1, col + 1),
        (row - 1, col + 1),
        (row, col),
        (row + 1, col - 1),
    ]


def get_word(matrix, indices) -> str | None:
    word = ""
    for idx in indices:
        if idx[0] < 0 or idx[0] >= len(matrix) or idx[1] < 0 or idx[1] >= len(matrix[0]):
            return None
        word += matrix[idx[0]][idx[1]]
    return word


def part1(data: str) -> Any:
    matrix = [[x for x in row] for row in data.splitlines()]

    xmas = []

    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            for idx in directions(row, col):
                word = get_word(matrix, idx)
                if word is not None and word == "XMAS":
                    xmas.append(idx)

    return len(xmas)


def part2(data: str) -> Any:
    matrix = [[x for x in row] for row in data.splitlines()]

    xmas = []

    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            dirs = mas_directions(row, col)
            word = get_word(matrix, dirs)
            if word and word.lower() in ["masmas", "samsam", "sammas", "massam"]:
                xmas.append(dirs)

    return len(xmas)


def main():
    parser = argparse.ArgumentParser(description="Process an input file.")
    parser.add_argument("input_file", type=str, help="Path to the input file")
    args = parser.parse_args()

    with open(args.input_file, "r") as file:
        data = file.read().strip()

    print(f"part1 -> {part1(data)}")
    print(f"part2 -> {part2(data)}")


if __name__ == "__main__":
    main()
