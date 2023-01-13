from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.signal_patterns = []
        data.outputs = []

        for row in lines:
            parts = row.split(' | ')
            patterns = [''.join(sorted(pattern)) for pattern in parts[0].split(' ')]
            row_outputs = [''.join(sorted(output)) for output in parts[1].split(' ')]

            data.signal_patterns.append(patterns)
            data.outputs.append(row_outputs)

    def compute(self, data):
        count = 0
        for row in data.outputs:
            for output in row:
                length = len(output)
                if length < 5 or length == 7:
                    count += 1

        return count

    def example_answer(self):
        return 26

    def example_input(self):
        return '''
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''


class PartB(PartA):
    def compute(self, data):
        output_sum = 0
        for patterns, outputs in zip(data.signal_patterns, data.outputs):
            digits = [''] * 10
            digits[1], digits[4], digits[7], digits[8] = self.find_unique(patterns)
            digits[6] = self.find_6(patterns, digits[1])
            digits[9] = self.find_9(patterns, digits[4])
            digits[0] = self.find_0(patterns, digits[6], digits[9])
            digits[3] = self.find_3(patterns, digits[1], digits[9])
            digits[5] = self.find_5(patterns, digits[6])
            digits[2] = self.find_2(patterns, digits[3], digits[5])

            lookup = {v: str(k) for k, v in enumerate(digits)}
            number = ''.join(lookup[output] for output in outputs)
            output_sum += int(number)

        return output_sum

    @staticmethod
    def find_unique(patterns):
        one = ''
        four = ''
        seven = ''
        eight = ''

        for pattern in patterns:
            if len(pattern) == 2:
                one = pattern
            elif len(pattern) == 3:
                seven = pattern
            elif len(pattern) == 4:
                four = pattern
            elif len(pattern) == 7:
                eight = pattern

        patterns.remove(one)
        patterns.remove(four)
        patterns.remove(seven)
        patterns.remove(eight)
        return one, four, seven, eight

    def find_6(self, patterns, one):
        for pattern in patterns:
            if len(pattern) != 6:
                continue
            if self.has_one(one, pattern):
                patterns.remove(pattern)
                return pattern

    def find_9(self, patterns, four):
        for pattern in patterns:
            if len(pattern) != 6:
                continue
            if self.has_all(four, pattern):
                patterns.remove(pattern)
                return pattern

    @staticmethod
    def find_0(patterns, six, nine):
        for pattern in patterns:
            if len(pattern) != 6:
                continue
            if pattern is not six and pattern is not nine:
                patterns.remove(pattern)
                return pattern

    def find_3(self, patterns, one, nine):
        for pattern in patterns:
            if len(pattern) != 5:
                continue
            if self.has_all(one, pattern) and self.has_all_but_one(nine, pattern):
                patterns.remove(pattern)
                return pattern

    def find_5(self, patterns, six):
        for pattern in patterns:
            if len(pattern) != 5:
                continue
            if self.has_all(pattern, six):
                patterns.remove(pattern)
                return pattern

    @staticmethod
    def find_2(patterns, three, five):
        for pattern in patterns:
            if len(pattern) != 5:
                continue
            if pattern is not three and pattern is not five:
                patterns.remove(pattern)
                return pattern

    # check if all chars are in string
    @staticmethod
    def has_all(chars, string):
        return all([char in string for char in chars])

    # check if one and only on char is in string
    @staticmethod
    def has_one(chars, string):
        checks = [char in string for char in chars]
        i = iter(checks)
        return any(i) and not any(i)

    # check if all but one char is in string
    @staticmethod
    def has_all_but_one(chars, string):
        checks = [char in string for char in chars]
        checks = [not check for check in checks]
        i = iter(checks)
        return any(i) and not any(i)

    def example_answer(self):
        return 61229


Day.do_day(8, 2021, PartA, PartB)
