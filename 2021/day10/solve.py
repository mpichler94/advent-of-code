from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.lines = text.splitlines()

    def compute(self, data):
        return sum(self.get_line_score(line) for line in data.lines)

    def get_line_score(self, line):
        score = {')': 3, ']': 57, '}': 1197, '>': 25137}
        stack = []
        for char in line:
            if not self.match_closing(char, stack):
                return score[char]
        return 0

    @staticmethod
    def match_closing(char, stack):
        matches = {'(': ')', '[': ']', '{': '}', '<': '>'}
        if char in ['(', '[', '{', '<']:
            stack.append(char)
        else:
            opening_char = stack.pop()
            needed = matches[opening_char]
            if char != needed:
                return False

        return True

    def example_answer(self):
        return 26397

    def example_input(self):
        return '''
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
'''


class PartB(PartA):
    def config(self, data):
        data.lines = filter(self.is_not_corrupt, data.lines)

    def compute(self, data):
        scores = [self.get_completion_score(line) for line in data.lines]
        scores.sort()
        return scores[len(scores) // 2]

    def is_not_corrupt(self, line):
        return self.get_line_score(line) == 0

    def get_completion_score(self, line):
        score = {'(': 1, '[': 2, '{': 3, '<': 4}
        stack = []

        [self.match_closing(char, stack) for char in line]
        points = 0
        stack.reverse()
        for char in stack:
            points = points * 5 + score[char]
        return points

    def example_answer(self):
        return 288957


Day.do_day(10, 2021, PartA, PartB)
