import argparse
from typing import Any
from itertools import combinations, count


def process_data(data: str) -> tuple[dict[str, Any], int, int]:
    nodes: dict[str, set[tuple[int, int]]] = {}
    rows = len(data.splitlines())
    cols = len(data.splitlines()[0])

    for r, line in enumerate(data.splitlines()):
        for c, char in enumerate(line):
            if char != ".":
                n = nodes.get(char, set())
                n.add((r, c))
                nodes[char] = n

    return nodes, rows, cols


# def dist(node1: tuple[int, int], node2: tuple[int, int]) -> int:
#     return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])


def vec(node1: tuple[int, int], node2: tuple[int, int]) -> tuple[int, int]:
    return (node2[0] - node1[0], node2[1] - node1[1])


def print_matrix(nodes, rows, cols):
    matrix = [["." for _ in range(cols)] for _ in range(rows)]

    for tup in nodes:
        r, c = tup[0]
        ca = tup[1]
        matrix[r][c] = ca

    for r in matrix:
        print("".join(r))


def antinodes_from(node: tuple[int, int], rows, cols, vec: tuple[int, int], infinite: bool) -> list[tuple[int, int]]:
    antinodes = []

    for i in count(1):
        nnode = (node[0] + i * vec[0], node[1] + i * vec[1])
        if not within_bounds(nnode, rows, cols):
            break
        else:
            antinodes.append(nnode)

        if not infinite:
            break

    return antinodes


def compute_antinodes(
    nodes: dict[str, set[tuple[int, int]]], rows: int, cols: int, repetition: bool
) -> list[tuple[tuple[int, int], Any]]:
    antinodes = []

    for k, antenas in nodes.items():
        for comb in combinations(antenas, 2):
            v = vec(comb[0], comb[1])
            node1 = (comb[1][0] + v[0], comb[1][1] + v[1])
            if within_bounds(node1, rows, cols):
                antinodes.append((node1, k))
            # print(f"combination {comb}, has vec: {v} and node1: {node1}")

            if repetition:
                for i in count(2):
                    nnode = (comb[1][0] + i * v[0], comb[1][1] + i * v[1])
                    if not within_bounds(nnode, rows, cols):
                        break
                    else:
                        antinodes.append((nnode, k))

            v_ = (-1 * v[0], -1 * v[1])
            node2 = (comb[0][0] + v_[0], comb[0][1] + v_[1])
            if within_bounds(node2, rows, cols):
                antinodes.append((node2, k))
            # print(f"combination {comb}, has vec: {v_} and node2: {node2}")

            if repetition:
                for i in count(2):
                    nnode = (comb[0][0] + i * v_[0], comb[0][1] + i * v_[1])
                    if not within_bounds(nnode, rows, cols):
                        break
                    else:
                        antinodes.append((nnode, k))

    return antinodes


def within_bounds(node: tuple[int, int], rows: int, cols: int) -> bool:
    return 0 <= node[0] < rows and 0 <= node[1] < cols


def dct_to_lst(matrix: dict[str, set[tuple[int, int]]]) -> list[tuple[Any, ...]]:
    rs = []
    for k, v in matrix.items():
        for t in v:
            rs.append((t, k))

    return rs


def part1(data: str) -> Any:
    nodes, rows, cols = process_data(data)

    print_matrix(dct_to_lst(nodes), rows, cols)
    print()

    antinodes = compute_antinodes(nodes, rows, cols, False)
    print_matrix(antinodes, rows, cols)

    return len(set([t[0] for t in antinodes]))


def part2(data: str) -> Any:
    nodes, rows, cols = process_data(data)

    print_matrix(dct_to_lst(nodes), rows, cols)
    print()

    antinodes = compute_antinodes(nodes, rows, cols, True)
    print_matrix(antinodes, rows, cols)

    return len(set([t[0] for t in antinodes]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=str)
    args = ap.parse_args()

    with open(args.input, "r") as f:
        data = f.read()

    print(f"part1 -> {part1(data)}")
    print(f"part2 -> {part2(data)}")
