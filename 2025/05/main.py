from typing import TypedDict


class Range(TypedDict):
    start: int
    end: int


def valInRange(rng: Range, val: int) -> bool:
    return rng["start"] <= val <= rng["end"]


class Db(TypedDict):
    Ranges: list[Range]
    Ids: list[int]


def read_input(file: str) -> Db:
    with open(file, "r") as h:
        data = h.read()

    ranges, ids = data.split("\n\n")

    idsParsed = list(map(int, ids.splitlines()))
    rangesParsed: list[Range] = []

    for r in ranges.splitlines():
        start, end = map(int, r.split("-"))
        rangesParsed.append(Range(start=start, end=end))

    return {"Ids": idsParsed, "Ranges": rangesParsed}


def solve(inp: Db) -> int:
    fresh = 0

    for id in inp["Ids"]:
        for r in inp["Ranges"]:
            if valInRange(r, id):
                fresh += 1
                break

    return fresh


def part1(file: str):
    inp = read_input(file)

    return solve(inp)


def part2(file: str):
    inp = read_input(file)

    inp["Ranges"] = sorted(inp["Ranges"], key=lambda r: r["start"])

    idx = 0
    chckIdx = idx + 1
    while True:
        if idx >= len(inp["Ranges"]):
            break

        if chckIdx >= len(inp["Ranges"]):
            break

        startWithin = inp["Ranges"][idx]["start"] <= inp["Ranges"][chckIdx]["start"] <= inp["Ranges"][idx]["end"]
        endWithin = inp["Ranges"][idx]["start"] <= inp["Ranges"][chckIdx]["end"] <= inp["Ranges"][idx]["end"]

        if startWithin and endWithin:
            inp["Ranges"].pop(chckIdx)
            continue

        if startWithin and not endWithin:
            inp["Ranges"][idx]["end"] = inp["Ranges"][chckIdx]["end"]
            inp["Ranges"].pop(chckIdx)
            continue

        idx += 1
        chckIdx = idx + 1

    return sum(map(lambda r: r["end"] - r["start"] + 1, inp["Ranges"]))


print(f"Part1 -> {part1('input.txt')}")
print(f"Part2 -> {part2('input.txt')}")
