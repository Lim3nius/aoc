import argparse
from typing import Any
from functools import reduce
from math import prod
from collections import defaultdict


def part1(data: str) -> Any:
    disk = []

    for i in range(0, len(data), 2):
        disk.extend([str(int(i / 2)) for _ in range(int(data[i]))])

        if i + 1 < len(data):
            disk.extend(["." for _ in range(int(data[i + 1]))])

    start = 0
    for i in range(len(disk) - 1, 0, -1):
        if disk[i] == ".":
            continue
        else:
            s = disk.index(".", start)
            if s > i:
                break

            disk[s], disk[i] = disk[i], disk[s]
            start = s + 1

    disk = disk[: disk.index(".")]
    return reduce(lambda acc, tup: acc + tup[0] * int(tup[1]), enumerate(disk), 0)


def part2(data: str) -> Any:
    disk = []

    space_groups: dict[int, list[tuple[int, int]]] = defaultdict(list)

    for i in range(0, len(data), 2):
        disk.extend([str(int(i / 2)) for _ in range(int(data[i]))])

        if i + 1 < len(data):
            size = int(data[i + 1])
            space_groups[size].append((len(disk), len(disk) + size))
            disk.extend(["." for _ in range(size)])

    c = len(disk) - 1
    while c > 0:
        if disk[c] == ".":
            c -= 1
            continue

        # some group
        grp_end = c + 1
        while c > 0 and disk[c] != "." and disk[c] == disk[grp_end - 1]:
            c -= 1

        grp_start = c + 1
        grp_sz = grp_end - grp_start

        # print(f"found group: {disk[grp_start:grp_end]}")

        # find earliest space to which group can fit
        pos = [k for k in space_groups.keys() if k >= grp_sz and len(space_groups.get(k, [])) > 0]
        if pos:
            win_space_sz = min(pos, key=lambda k: space_groups[k][0][0])
            win_space = space_groups[win_space_sz].pop(0)

            # print(f"selected space: {win_space}")

            if win_space[0] > grp_start:
                # print("space is closer to end")
                continue

            win_space_sz = win_space[1] - win_space[0]

            disk[win_space[0] : win_space[0] + grp_sz] = disk[grp_start:grp_end]
            disk[grp_start:grp_end] = ["." for _ in range(grp_sz)]

            if win_space_sz > grp_sz:
                new_space = (win_space[0] + grp_sz, win_space[1])
                new_space_sz = win_space_sz - grp_sz

                space_groups[new_space_sz].append(new_space)
                space_groups[new_space_sz].sort(key=lambda tup: tup[0])

    return reduce(lambda acc, tup: acc + tup[0] * int(tup[1] if tup[1] != "." else 0), enumerate(disk), 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="Path to input file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = f.read().strip()

    print(f"part1 -> {part1(data)}")
    print(f"part2 -> {part2(data)}")
