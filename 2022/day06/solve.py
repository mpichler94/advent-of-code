from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.stream = text

    def compute(self, data):
        for i in range(3, len(data.stream)):
            marker = set(data.stream[i-3:i+1])
            if len(marker) == 4:
                return i + 1

        raise RuntimeError('No start of packet marker found')

    def example_answer(self):
        return 7

    def tests(self):
        yield "bvwbjplbgvbhsrlpgdmjqwftvncz", 5, "Example2"
        yield "nppdvjthqldpwncqszvftbrmjlhg", 6, "Example3"
        yield "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, "Example4"
        yield "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, "Example5"


class PartB(PartA):
    def compute(self, data):
        sop = PartA.compute(self, data) - 5
        for i in range(sop + 13, len(data.stream)):
            marker = set(data.stream[i-13:i+1])
            if len(marker) == 14:
                return i + 1

        raise RuntimeError('No start of packet marker found')

    def example_answer(self):
        return 19

    def tests(self):
        yield "bvwbjplbgvbhsrlpgdmjqwftvncz", 23, "Example2"
        yield "nppdvjthqldpwncqszvftbrmjlhg", 23, "Example3"
        yield "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29, "Example4"
        yield "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26, "Example5"


Day.do_day(6, 2022, PartA, PartB)
