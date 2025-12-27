from dataclasses import dataclass
import math


@dataclass(frozen=True, eq=True)
class Coord:
    x: int
    y: int
    z: int


@dataclass
class Distance:
    junctionBox1: Coord
    junctionBox2: Coord
    dist: float


def readInput(file: str) -> list[Coord]:
    data: list[Coord] = []

    with open(file, "r") as h:
        for ln in h:
            x, y, z = map(int, ln.split(","))
            data.append(Coord(x, y, z))

    return data


def calcDistance(jb1: Coord, jb2: Coord) -> float:
    return math.sqrt((jb2.x - jb1.x) ** 2 + (jb2.y - jb1.y) ** 2 + (jb2.z - jb1.z) ** 2)


def calculateSortedDistances(coords: list[Coord]) -> list[Distance]:
    distances: list[Distance] = []

    for i in range(len(coords) - 1):
        for j in range(i + 1, len(coords)):
            dd = calcDistance(coords[i], coords[j])
            distances.append(Distance(coords[i], coords[j], dd))

    return sorted(distances, key=lambda e: e.dist)


def initializeCircuits(coords: list[Coord]) -> tuple[dict[str, set[Coord]], dict[Coord, str]]:
    circuits: dict[str, set[Coord]] = {}
    jbMapToCircuits: dict[Coord, str] = {}

    for c in coords:
        circName = f"circuit-{len(circuits)}"
        circuits[circName] = set([c])
        jbMapToCircuits[c] = circName

    return circuits, jbMapToCircuits


def mergeCircuits(
    circuits: dict[str, set[Coord]],
    jbMapToCircuits: dict[Coord, str],
    jb1: Coord,
    jb2: Coord,
) -> bool:
    newCircName = jbMapToCircuits[jb2]
    oldCircName = jbMapToCircuits[jb1]

    if oldCircName == newCircName:
        return False

    connCircuit = circuits[newCircName]

    for jbox in circuits[oldCircName]:
        jbMapToCircuits[jbox] = newCircName
        connCircuit.add(jbox)

    circuits[newCircName] = connCircuit
    circuits[oldCircName] = set()

    return True


def part1(file: str):
    coords = readInput(file)
    distances = calculateSortedDistances(coords)
    circuits, jbMapToCircuits = initializeCircuits(coords)

    i = 0
    for d in distances:
        if i == 1000:
            break

        if mergeCircuits(circuits, jbMapToCircuits, d.junctionBox1, d.junctionBox2):
            i += 1

    sortedCircuitsSizes = sorted([len(v) for v in circuits.values()], reverse=True)
    return math.prod(sortedCircuitsSizes[:3])


def part2(file: str):
    coords = readInput(file)
    distances = calculateSortedDistances(coords)
    circuits, jbMapToCircuits = initializeCircuits(coords)

    circuitCount = len(circuits)

    for d in distances:
        if mergeCircuits(circuits, jbMapToCircuits, d.junctionBox1, d.junctionBox2):
            circuitCount -= 1

            if circuitCount == 1:
                return d.junctionBox1.x * d.junctionBox2.x


print(f"Part1 -> {part1('input.txt')}")
print(f"Part2 -> {part2('input.txt')}")
