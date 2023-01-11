from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.rucksacks = [line for line in text.splitlines()]

    def compute(self, data):
        sum = 0
        for rucksack in data.rucksacks:
            compartment1 = set(rucksack[0:len(rucksack) // 2])
            compartment2 = set(rucksack[len(rucksack) // 2:])

            both = compartment1.intersection(compartment2)
            if len(both) > 0:
                char = both.pop()
                sum += self.convert_to_num(char)

        return sum

    @staticmethod
    def convert_to_num(char):
        if char.isupper():
            return ord(char) - 65 + 27
        else:
            return ord(char) - 97 + 1

    def example_answer(self):
        return 157


class PartB(PartA):
    def compute(self, data):
        sum = 0
        for i in range(0, len(data.rucksacks), 3):
            rucksack1 = set(data.rucksacks[i])
            rucksack2 = set(data.rucksacks[i + 1])
            rucksack3 = set(data.rucksacks[i + 2])

            badge = rucksack1.intersection(rucksack2)
            badge = badge.intersection(rucksack3)

            if len(badge) > 0:
                sum += self.convert_to_num(badge.pop())

        return sum

    def example_answer(self):
        return 70


Day.do_day(3, 2022, PartA, PartB)
