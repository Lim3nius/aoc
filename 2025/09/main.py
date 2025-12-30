type Coord = tuple[int, int]


def readInput(file: str) -> list[Coord]:
    tiles: list[Coord] = []

    with open(file, "r") as h:
        for ln in h:
            x, y = map(int, ln.strip().split(","))
            tiles.append((x, y))

    return tiles


def computeArea(p1: Coord, p2: Coord) -> int:
    return (abs(p2[0] - p1[0]) + 1) * (abs(p2[1] - p1[1]) + 1)


def part1(file: str) -> int:
    tileCoords = readInput(file)

    areas: list[int] = []

    for i in range(len(tileCoords) - 1):
        for j in range(i + 1, len(tileCoords)):
            area = computeArea(tileCoords[i], tileCoords[j])
            areas.append(area)

    areas = sorted(areas)
    return areas[-1]


type Point = tuple[int, int]


def isRectangleWithinBounds(jb1: Point, jb2: Point, okMap: list[list[int]]) -> bool:
    botLeft: Point = (min(jb1[0], jb2[0]), min(jb1[1], jb2[1]))
    topRight: Point = (max(jb1[0], jb2[0]), max(jb1[1], jb2[1]))

    topLeft = (topRight[0], botLeft[1])
    botRight = (botLeft[0], topRight[1])

    for i in range(topRight[0] - botLeft[0] + 1):
        boundsInside = okMap[botLeft[0] + i][botLeft[1]] >= 0 and okMap[botRight[0] + i][botRight[1]] >= 0

        if not boundsInside:
            return False

    for i in range(topRight[1] - botLeft[1] + 1):
        boundsInside = okMap[topLeft[0]][topLeft[1] + i] >= 0 and okMap[botLeft[0]][botLeft[1] + i] >= 0
        if not boundsInside:
            return False

    return True


def part2(file: str) -> int:
    tileCoords = readInput(file)

    rows = sorted(set([t[0] for t in tileCoords]))
    cols = sorted(set([t[1] for t in tileCoords]))

    reverseRowRDs = {v: i for i, v in enumerate(rows)}
    reverseColRDs = {v: i for i, v in enumerate(cols)}

    reducedTiles = [(reverseRowRDs[t[0]], reverseColRDs[t[1]]) for t in tileCoords]
    reducedMap = [[0 for _ in range(len(reverseColRDs))] for _ in range(len(reverseRowRDs))]

    # mark reduced tiles in map
    for rt in reducedTiles:
        reducedMap[rt[0]][rt[1]] = 1

    tmap = reducedTiles[:]
    tmap.append(tmap[0])
    # fill in boundaries to map
    for i in range(len(tmap) - 1):
        ri, rj = tmap[i], tmap[i + 1]

        if ri[0] == rj[0]:
            inc = -1 if ri[1] > rj[1] else 1
            off = 0
            while ri[1] + off != rj[1]:
                if reducedMap[ri[0]][ri[1] + off] == 0:
                    reducedMap[ri[0]][ri[1] + off] = 2
                off += inc

        elif ri[1] == rj[1]:
            inc = -1 if ri[0] > rj[0] else 1
            off = 0
            while ri[0] + off != rj[0]:
                if reducedMap[ri[0] + off][ri[1]] == 0:
                    reducedMap[ri[0] + off][ri[1]] = 2
                off += inc
        else:
            raise Exception("wtf?")

    # flood fill empty space
    emptySpace: set[tuple[int, int]] = set()
    for i in range(len(reducedMap)):
        for j in [0, len(reducedMap[i]) - 1]:
            if reducedMap[i][j] == 0:
                emptySpace.add((i, j))

    while emptySpace:
        nextEmptySpace: set[tuple[int, int]] = set()
        for es in emptySpace:
            reducedMap[es[0]][es[1]] = -1
            for dr in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                if not (0 <= es[0] + dr[0] < len(reducedMap)) or not (0 <= es[1] + dr[1] < len(reducedMap[0])):
                    continue

                if reducedMap[es[0] + dr[0]][es[1] + dr[1]] == 0:
                    nextEmptySpace.add((es[0] + dr[0], es[1] + dr[1]))
        emptySpace = nextEmptySpace

    def printMap():
        for r in reducedMap:
            print("".join([f"{v: 3}" for v in r]))

    # printMap()

    areas: list[int] = []

    reducedRowToReal = {v: k for k, v in reverseRowRDs.items()}
    reducedColToReal = {v: k for k, v in reverseColRDs.items()}

    for i in range(len(reducedTiles) - 1):
        for j in range(i, len(reducedTiles)):
            if isRectangleWithinBounds(reducedTiles[i], reducedTiles[j], reducedMap):
                realTileI = (reducedRowToReal[reducedTiles[i][0]], reducedColToReal[reducedTiles[i][1]])
                realTileJ = (reducedRowToReal[reducedTiles[j][0]], reducedColToReal[reducedTiles[j][1]])

                area = computeArea(realTileI, realTileJ)
                areas.append(area)

    areas = sorted(areas)
    return areas[-1]


print(f"part1 -> {part1('input.txt')}")
print(f"part2 -> {part2('input.txt')}")
