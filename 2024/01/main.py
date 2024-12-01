from argparse import ArgumentParser
from collections import Counter


def process(input: str) -> (list[int], list[int]):
    left_list = []
    right_list = []

    for ln in input.splitlines():
        if not ln:
            continue

        left, right = ln.split()
        left_list.append(int(left))
        right_list.append(int(right))

    return left_list, right_list


def part1(input: str):
    left_list, right_list = process(input)

    left_list = sorted(left_list)
    right_list = sorted(right_list)

    return sum(map(lambda tup: abs(tup[0] - tup[1]), zip(left_list, right_list)))


def part2(input: str):
    left_list, right_list = process(input)

    left_list = sorted(left_list)
    right_counter = Counter(right_list)

    return sum(map(lambda i: i * right_counter[i], left_list))


def main():
    ap = ArgumentParser(description="Advent of Code 2024 - Day 1")
    ap.add_argument("input", help="Input file")
    args = ap.parse_args()

    with open(args.input) as f:
        data = f.read().strip()

    print(f"part1 -> {part1(data)}")
    print(f"part2 -> {part2(data)}")


if __name__ == "__main__":
    main()
