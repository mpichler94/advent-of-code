from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.numbers = [int(num) for num in text.split(",")]
        data.target = 2020

    def compute(self, data):
        seen = {}
        last_num = 0
        for i in range(data.target):
            if i < len(data.numbers):
                seen[data.numbers[i]] = (i, 0)
                last_num = data.numbers[i]
                continue

            if last_num in seen:
                num = seen[last_num][1]
                last_num = num
                if num in seen:
                    turn, _ = seen[num]
                    seen[num] = (i, i - turn)
                else:
                    seen[num] = (i, 0)
            elif 0 in seen:
                seen[last_num] = (i, 0)
                turn, dist = seen[0]
                seen[0] = (i, i - turn)
                last_num = 0
            else:
                seen[last_num] = (i, 0)
                seen[0] = (i, 0)
                last_num = 0

        return last_num

    def example_input(self):
        return "0,3,6"

    def example_answer(self):
        return 436

    def tests(self):
        yield "1,3,2", 1, ""
        yield "2,1,3", 10, ""
        yield "1,2,3", 27, ""
        yield "2,3,1", 78, ""
        yield "3,2,1", 438, ""
        yield "3,1,2", 1836, ""


class PartB(PartA):
    def config(self, data):
        data.target = 30000000

    def example_answer(self):
        return 175594

    def tests(self):
        yield "1,3,2", 2578, ""
        yield "2,1,3", 3544142, ""
        yield "1,2,3", 261214, ""
        yield "2,3,1", 6895259, ""
        yield "3,2,1", 18, ""
        yield "3,1,2", 362, ""


Day.do_day(15, 2020, PartA, PartB)
