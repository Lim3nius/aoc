import argparse
from typing import Any
import sys


def is_correct(page: list[int], rules: dict[int, set[int]]) -> bool:
    for i in range(len(page)):
        if set(page[:i]).intersection(rules.get(page[i], set())):
            return False
    return True


def select_correct(pages: list[list[int]], rules: dict[int, set[int]]) -> list[list[int]]:
    correct_pages = []
    for page in pages:
        if is_correct(page, rules):
            correct_pages.append(page)

    return correct_pages


def parse_input(data: str) -> tuple[dict[int, set[int]], list[list[int]]]:
    rules, pages = data.split("\n\n")

    rule_dict: dict[int, set[int]] = {}
    for ln in rules.splitlines():
        k, v = map(int, ln.split("|"))
        s = rule_dict.get(k, set())
        s.add(v)
        rule_dict[k] = s

    parsed_pages = [list(map(int, ln.split(","))) for ln in pages.splitlines()]

    return rule_dict, parsed_pages


def fix_page(rules: dict[int, set[int]], page: list[int]) -> list[int]:
    fixed_page = []
    working_page = set(page)

    while len(working_page) > 0:
        tup = max([(num, working_page.intersection(rules.get(num, set()))) for num in working_page], key=lambda x: x[1])
        fixed_page.append(tup[0])
        working_page.remove(tup[0])

    if not is_correct(fixed_page, rules):
        print("page is not fixed: {fixed_page}")
        sys.exit(1)

    return fixed_page


def part1(data: str) -> Any:
    rules, pages = parse_input(data)
    correct_pages = select_correct(pages, rules)
    # print(correct_pages)

    return sum(p[int(len(p) / 2)] for p in correct_pages)


def part2(data: str) -> Any:
    rules, pages = parse_input(data)

    bad_pages = filter(lambda p: not is_correct(p, rules), pages)
    fixed_pages = [fix_page(rules, p) for p in bad_pages]

    return sum(p[int(len(p) / 2)] for p in fixed_pages)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="file with input data")
    args = ap.parse_args()

    with open(args.input) as f:
        data = f.read().strip()

    print(f"part1 -> {part1(data)}")
    print(f"part1 -> {part2(data)}")


if __name__ == "__main__":
    main()
