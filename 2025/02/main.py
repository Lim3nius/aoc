from dataclasses import dataclass
from collections import Counter


@dataclass
class Range:
    start: int
    end: int


def read_input(file: str) -> list[Range]:
    with open(file, "r") as h:
        data = h.readlines()

    assert len(data) == 1

    res: list[Range] = []

    for rang in data[0].split(","):
        start, end = rang.split("-")
        res.append(Range(start=int(start), end=int(end)))

    return res


def invalids_in_range(r: Range) -> list[int]:
    invalids: list[int] = []

    for i in range(r.start, r.end + 1):
        txt_repr = str(i)
        if len(txt_repr) % 2 == 1:
            continue

        half = len(txt_repr) // 2
        invalid = txt_repr[0:half] == txt_repr[half:]
        if invalid:
            invalids.append(i)

    return invalids


def invalid_v2(r: Range) -> list[int]:
    invalids: list[int] = []

    for i in range(r.start, r.end + 1):
        txt_repr = str(i)
        if len(txt_repr) % 2 == 1:
            c = Counter(txt_repr)
            if len(c.keys()) == 1:
                invalids.append(i)
                continue

        half = len(txt_repr) // 2
        for j in range(1, half + 1):
            if len(txt_repr) % j != 0:
                continue

            chunk0 = txt_repr[0:j]
            chunks = (txt_repr[x : x + j] for x in range(0, len(txt_repr), j))
            if all(x == chunk0 for x in chunks):
                invalids.append(i)
                break

    return invalids


def part1(file: str) -> int:
    ranges = read_input(file)
    total_invalids: list[int] = []

    for r in ranges:
        invalids = invalids_in_range(r)
        total_invalids.extend(invalids)

    return sum(total_invalids)


def part2(file: str) -> int:
    ranges = read_input(file)
    total_invalids: list[int] = []

    for r in ranges:
        invalids = invalid_v2(r)
        total_invalids.extend(invalids)

    return sum(total_invalids)


print(f"Part1 -> {part1('input.txt')}")
print(f"Part1 -> {part2('input.txt')}")
