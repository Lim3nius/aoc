def read_input(file: str) -> list[list[int]]:
    banks: list[list[int]] = []

    with open(file, "r") as h:
        for ln in h:
            ln = ln.strip()
            banks.append(list(map(int, list(ln))))

    return banks


def highhest_joltage_for_n(bank: list[int], remaining_numbers: int) -> list[int]:
    if remaining_numbers == 0:
        return []

    max_joltage_idx = 0
    for idx in range(0, len(bank) - (remaining_numbers - 1)):
        if bank[idx] > bank[max_joltage_idx]:
            max_joltage_idx = idx

    nums = highhest_joltage_for_n(bank[max_joltage_idx + 1 :], remaining_numbers - 1)
    nums.insert(0, bank[max_joltage_idx])

    return nums


def part1(input: str, max_n_nums: int) -> int:
    banks = read_input(input)

    joltage_sum = 0
    for b in banks:
        joltages = highhest_joltage_for_n(b, max_n_nums)
        val = int("".join(map(str, joltages)))

        joltage_sum += val

    return joltage_sum


print(f"Part1 -> {part1('input.txt', 2)}")
print(f"Part2 -> {part1('input.txt', 12)}")
