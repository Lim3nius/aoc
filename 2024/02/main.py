from argparse import ArgumentParser
from typing import Any
from functools import reduce


def preprocess(data: str) -> Any:
    reports = []

    for ln in data.splitlines():
        reports.append(list(map(int, ln.split())))

    return reports


def gen_mutations(lst: list[int]) -> list[list[int]]:
    res = []
    for i in range(len(lst)):
        res.append(lst[:i] + lst[i + 1 :])

    return res


def compute_diffs(report: list[int]) -> list[int]:
    return list(map(lambda tup: tup[1] - tup[0], zip(report, report[1:])))


def diffs_in_report_ok(diffs: list[int]) -> bool:
    first = diffs[0]
    for d in diffs:
        if not (1 <= abs(d) <= 3):
            return False

        if first > 0 and d < 0:
            return False
        elif first < 0 and d > 0:
            return False

    return True


def part1(data: str) -> Any:
    reports = preprocess(data)

    ok_reports = []
    fail_reports = []

    for report in reports:
        diffs = compute_diffs(report)

        if diffs_in_report_ok(diffs):
            ok_reports.append(report)
        else:
            fail_reports.append(report)

    return len(ok_reports)


def part2(data: str) -> Any:
    reports = preprocess(data)

    ok_reports = []
    fail_reports = []

    for report in reports:
        rep_mutations = [report]
        rep_mutations.extend(gen_mutations(report))

        if any(diffs_in_report_ok(compute_diffs(m)) for m in rep_mutations):
            ok_reports.append(report)
        else:
            fail_reports.append(report)

    return len(ok_reports)


def main():
    ap = ArgumentParser(description="Advent of Code 2024 - Day 2")
    ap.add_argument("input", help="Input file")
    args = ap.parse_args()

    with open(args.input) as f:
        data = f.read().strip()

    print(f"part1 -> {part1(data)}")
    print(f"part2 -> {part2(data)}")


if __name__ == "__main__":
    main()
