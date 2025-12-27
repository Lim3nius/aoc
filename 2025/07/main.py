from functools import cache


def readInput(file: str) -> list[list[str]]:
    with open(file, "r") as h:
        data = [list(ln.strip()) for ln in h]

    return data


def countSplits(mat: list[list[str]]):
    startIdx = mat[0].index("S")

    visited: dict[tuple[int, int], bool] = {}

    def traverse(row: int, col: int) -> int:
        if row >= len(mat):
            return 0

        if not (0 <= col <= len(mat[row])):
            raise Exception("getting out of the bounds")

        match mat[row][col]:
            case "^":
                if visited.get((row, col)):
                    return 0

                visited[(row, col)] = True

                return 1 + traverse(row, col - 1) + traverse(row, col + 1)
            case "S" | ".":
                return traverse(row + 1, col)
            case _:
                raise Exception(f"I messed up: I am at {mat[row][col]}")

    return traverse(0, startIdx)


def countPaths(mat: list[list[str]]) -> int:
    startIdx = mat[0].index("S")

    @cache
    def solve(row: int, col: int) -> int:
        if row >= len(mat):
            return 1

        if not (0 <= col <= len(mat[row])):
            raise Exception("getting out of the bounds")

        match mat[row][col]:
            case "^":
                return solve(row, col - 1) + solve(row, col + 1)
            case "S" | ".":
                return solve(row + 1, col)
            case _:
                raise Exception(f"I messed up: I am at {mat[row][col]}")

    return solve(0, startIdx)


def part1(file: str):
    inp = readInput(file)

    return countSplits(inp)


def part2(file: str):
    inp = readInput(file)

    return countPaths(inp)


print(f"Part1 -> {part1('input.txt')}")
print(f"Part2 -> {part2('input.txt')}")
