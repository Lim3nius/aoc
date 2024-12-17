import argparse
from typing import Any
from dataclasses import dataclass
import re


@dataclass
class Problem:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]

    def part2_increase(self):
        self.prize = (self.prize[0] + 10_000_000_000_000, self.prize[1] + 10_000_000_000_000)

    def solve_for_cheap(self, max_presses=True) -> tuple[int, int] | None:
        # print(f"solving: {self}")

        i = self.prize[0] // self.button_b[0]
        j = self.prize[1] // self.button_b[1]

        start = min(i, j)
        if max_presses:
            start = min(start, 100)

        for i in range(start, -1, -1):
            # print(f"i: {i}")
            a0 = self.prize[0] - i * self.button_b[0]
            a1 = self.prize[1] - i * self.button_b[1]

            if a0 % self.button_a[0] == 0:
                x = a0 // self.button_a[0]

                if a1 - x * self.button_a[1] == 0:
                    return (x, i)

        return None


def parse_problems(input: str) -> list[Problem]:
    problems: list[Problem] = []

    def parse_button(button: str) -> tuple[int, int]:
        res = re.findall(r"\d+", button)
        assert len(res) == 2

        return tuple(map(int, res))  # type: ignore

    for prob in input.split("\n\n"):
        but_a, but_b, prize = prob.splitlines()
        problems.append(
            Problem(
                button_a=parse_button(but_a),
                button_b=parse_button(but_b),
                prize=parse_button(prize),
            )
        )

    return problems


def part1(input: str) -> Any:
    problems = parse_problems(input)

    tot = 0
    for prob in problems:
        if res := prob.solve_for_cheap():
            print(f"solved: {prob}, {res}")
            tot += res[0] * 3 + res[1]

    return tot


def part2(input: str) -> Any:
    problems = parse_problems(input)

    for p in problems:
        p.part2_increase()
        print(p)

    tot = 0
    for prob in problems:
        if res := prob.solve_for_cheap():
            print(f"solved: {prob}, {res}")
            tot += res[0] * 3 + res[1]

    return tot


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file")
    args = parser.parse_args()

    with open(args.input) as f:
        input = f.read().strip()

    print(f"Part1 -> {part1(input)}")
    print(f"Part2 -> {part2(input)}")
