import re
from utils.aoc_base import Day


class PartA(Day):
    def compute(self, data):
        memory = {}
        or_mask = 0
        and_mask = 0
        for line in data.text.splitlines():
            if line.startswith("mask"):
                or_mask, and_mask = self.get_masks(line)
            else:
                addr, num = self.parse_instruction(line)
                memory[addr] = (num & and_mask) | or_mask

        return sum(memory.values())

    @staticmethod
    def get_masks(line):
        mask = line[7:]
        or_mask = int(mask.replace("X", "0"), base=2)
        and_mask = int(mask.replace("X", "1"), base=2)
        return or_mask, and_mask

    @staticmethod
    def parse_instruction(line):
        match = re.match(r"mem\[(\d+)\] = (\d+)", line)
        addr = int(match.group(1))
        num = int(match.group(2))
        return addr, num

    def example_answer(self):
        return 165


class PartB(PartA):
    def compute(self, data):
        memory = {}
        mask = ""
        for line in data.text.splitlines():
            if line.startswith("mask"):
                mask = line[7:]
            else:
                addr, num = self.parse_instruction(line)
                addresses = self.apply_mask(mask, addr)
                for a in addresses:
                    memory[int(a, base=2)] = num

        return sum(memory.values())

    @staticmethod
    def apply_mask(mask, addr):
        addr = f"{addr:036b}"
        for i in range(36):
            if mask[i] == "1":
                addr = addr[:i] + "1" + addr[i + 1 :]
        addresses = [addr]
        for i in range(36):
            if mask[i] == "X":
                for j in range(len(addresses)):
                    tmp = addresses[j][:i] + "1" + addresses[j][i + 1 :]
                    addresses.append(tmp)
                    tmp = addresses[j][:i] + "0" + addresses[j][i + 1 :]
                    addresses.append(tmp)

        return addresses

    def example_answer(self):
        return 208

    def example_input(self):
        return """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""


Day.do_day(14, 2020, PartA, PartB)
