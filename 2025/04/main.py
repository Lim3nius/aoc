type Matrix = list[list[str]]


def read_input(file: str) -> Matrix:
    matrix: list[list[str]] = []
    with open(file, "r") as h:
        for ln in h:
            matrix.append(list(ln.strip()))
    return matrix


def neighboring_rolls(mat: Matrix, row: int, col: int) -> list[tuple[int, int]]:
    rolls: list[tuple[int, int]] = []
    for ri in [-1, 0, 1]:
        for ci in [-1, 0, 1]:
            if ci == 0 and ri == 0:
                continue

            if not ((0 <= row + ri < len(mat)) and (0 <= col + ci < len(mat[row]))):
                continue

            if mat[row + ri][col + ci] == "@":
                rolls.append((row + ri, col + ci))

    return rolls


def solve(mat: Matrix) -> list[tuple[int, int]]:
    rolls: list[tuple[int, int]] = []

    for row in range(0, len(mat)):
        for col in range(0, len(mat[row])):
            if mat[row][col] != "@":
                continue

            if len(neighboring_rolls(mat, row, col)) < 4:
                rolls.append((row, col))
    return rolls


def part1(file: str) -> int:
    inp = read_input(file)

    return len(solve(inp))


def part2(file: str) -> int:
    inp = read_input(file)

    totalRemoved = 0

    while True:
        removed = solve(inp)
        totalRemoved += len(removed)

        if len(removed) == 0:
            break

        for pos in removed:
            inp[pos[0]][pos[1]] = "."

    return totalRemoved


print(f"Part1 -> {part1('input.txt')}")
print(f"Part2 -> {part2('input.txt')}")
