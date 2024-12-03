import re
import argparse
from math import prod
from functools import reduce


mul_re = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

match_disabled = re.compile(r"don't\(\).+do\(\)")  # baaaaad

doRe = re.compile(r"do\(\)")
dontRe = re.compile(r"don't\(\)")


def part1(data: str) -> int:
    matches = mul_re.findall(data)

    return reduce(lambda acc, e: acc + prod(map(int, e)), matches, 0)


def part2(data: str):
    cop = data[:]
    to_eval = []

    while len(cop) > 0:
        m = dontRe.search(cop)
        if m:
            to_eval.append(cop[: m.start()])
            cop = cop[m.end() :]

            m = doRe.search(cop)
            if m:
                cop = cop[m.end() :]
            else:
                cop = ""
        else:
            to_eval.append(cop)
            cop = ""

    return sum(
        reduce(lambda acc, e: acc + prod(map(int, e)), mul_re.findall(m), 0)
        for m in to_eval
    )


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
