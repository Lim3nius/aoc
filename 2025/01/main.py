from typing import Literal, cast

Dir = Literal["L", "R"]


def rotate(dir: Literal["L", "R"], amount: int):
    global start
    match dir:
        case "L":
            start -= amount
            if start < 0:
                start = abs(start)
                start = 100 - (start % 100)
        case "R":
            start += amount

    start = start % 100

def rotate2(dir: Literal["L", "R"], amount: int):
    global start2
    global cntr2
    if (cnt := amount // 100) >= 1:
        cntr2 += cnt

    amount = amount % 100

    match dir:
        case "L":
            if amount > start2 and start2 != 0:
                # print(f'adding L{amount} to {start2}, increasing by 1')
                cntr2 += 1

            start2 -= amount
            if start2 < 0:
                start2 = abs(start2)
                start2 = 100 - (start2 % 100)

        case "R":
            if amount > (100 - start2) and start2 != 0:
                # print(f'adding R{amount} to {start2}, increasing by 1')
                cntr2 += 1

            start2 += amount

    start2 = start2 % 100


start2 = 50
cntr2 = 0

start = 50
cntr = 0

with open("input.txt", "r") as h:
    for ln in h:
        ln = ln.strip()
        dir = ln[0]
        rot = int(ln[1:])

        if dir not in ["L", "R"]:
            raise Exception()

        prev = start
        dir = cast(Dir, dir)
        rotate(dir, rot)
        rotate2(dir, rot)
        # print(f"{ln} -> {dir} {rot}, {prev} -> {start}")
        # input()

        if start == 0:
            cntr += 1

        if start2 == 0:
            cntr2 += 1

print(f"Part 1 -> {cntr}")
print(f"Part 2 -> {cntr2}")
