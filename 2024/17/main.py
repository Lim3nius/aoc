import argparse
from typing import Any
import re


class machine:
    registerA: int
    registerB: int
    registerC: int
    program: list[int]
    pc = 0
    jump = False

    def __init__(self, program: list[int], rega: int = 0, regb: int = 0, regc: int = 0):
        self.registerA = rega
        self.registerB = regb
        self.registerC = regc
        self.program = program
        self.buf = []

    def adv(self, combo_op: int):
        val = self.resolve_combo(combo_op)
        res = self.registerA / (2**val)
        self.registerA = int(res)

    def bxl(self, literal: int):
        self.registerB = self.registerB ^ literal

    def bst(self, combo_op: int):
        val = self.resolve_combo(combo_op)
        res = val % 8
        self.registerB = res

    def jnz(self, literal: int):
        if self.registerA == 0:
            return

        self.pc = literal
        self.jump = True

    def bxc(self, literal: int):
        _ = literal  # unused
        self.registerB = self.registerB ^ self.registerC

    def out(self, combo_op: int):
        val = self.resolve_combo(combo_op) % 8
        self.buf.append(val)
        # print(f"{val},", end="", flush=True)

    def bdv(self, combo_op: int):
        val = self.resolve_combo(combo_op)
        res = self.registerA / (2**val)
        self.registerB = int(res)

    def cdf(self, combo_op: int):
        val = self.resolve_combo(combo_op)
        res = self.registerA / (2**val)
        self.registerC = int(res)

    def resolve_combo(self, combo_op: int) -> int:
        match combo_op:
            case 0 | 1 | 2 | 3:
                return combo_op
            case 4:
                return self.registerA
            case 5:
                return self.registerB
            case 6:
                return self.registerC
            case 7:
                raise ValueError("7 compo op is reserved")
            case _:
                raise ValueError("Invalid combo_op")

    def run(self, buf: list[int]):
        self.buf = buf
        while self.pc < len(self.program):
            self.jump = False
            instr = self.program[self.pc]
            arg = self.program[self.pc + 1]

            match instr:
                case 0:
                    self.adv(arg)
                case 1:
                    self.bxl(arg)
                case 2:
                    self.bst(arg)
                case 3:
                    self.jnz(arg)
                case 4:
                    self.bxc(arg)
                case 5:
                    self.out(arg)
                case 6:
                    self.bdv(arg)
                case 7:
                    self.cdf(arg)
                case _:
                    raise ValueError(f"Invalid instruction: {instr}")

            if not self.jump:
                self.pc += 2


def parse_input(input: str) -> machine:
    regs, prog = input.split("\n\n")

    def parse_reg(reg: str) -> int:
        m = re.findall(r"-?\d+", reg.strip())
        assert len(m) == 1
        return int(m[0])

    a, b, c = regs.splitlines()
    ra = parse_reg(a)
    rb = parse_reg(b)
    rc = parse_reg(c)

    _, prog = prog.split(" ")
    pr = list(map(int, prog.strip().split(",")))
    return machine(pr, ra, rb, rc)


def part1(input: str) -> Any:
    mach = parse_input(input)
    res: list[int] = []
    mach.run(res)
    return ",".join(map(str, res))


def part2(input: str) -> Any:
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file")
    args = parser.parse_args()

    with open(args.input) as f:
        input_ = f.read().strip()

    print(f"Part1 -> {part1(input_)}")
    print(f"Part2 -> {part2(input_)}")
