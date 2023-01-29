from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.instructions = []
        for line in text.splitlines():
            data.instructions.append((line[:3], int(line[4:])))

    def compute(self, data):
        _, acc = self.execute(data.instructions)
        return acc

    @staticmethod
    def execute(instructions):
        executed = set()
        acc = 0
        pc = 0
        while True:
            if pc >= len(instructions) or pc in executed:
                break
            cmd, arg = instructions[pc]
            executed.add(pc)
            pc += 1
            if cmd == "acc":
                acc += arg
            elif cmd == "jmp":
                pc += arg - 1

        return pc, acc

    def example_answer(self):
        return 5


class PartB(PartA):
    def compute(self, data):
        changed_idx = 0
        for i in range(len(data.instructions)):
            instructions = self.change(data.instructions, i)
            pc, acc = self.execute(instructions)
            if pc >= len(data.instructions):
                return acc

    @staticmethod
    def change(instructions, idx):
        tmp = list(instructions)
        cmd, arg = instructions[idx]
        if cmd == "nop":
            cmd = "jmp"
        elif cmd == "jmp":
            cmd = "nop"
        tmp[idx] = (cmd, arg)
        return tmp

    def example_answer(self):
        return 8


Day.do_day(8, 2020, PartA, PartB)
