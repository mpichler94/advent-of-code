from utils.aoc_base import Day
import pyparsing as pp


class PartA(Day):
    def parse(self, text, data):
        data.expressions = text.splitlines()

        pp.ParserElement.enablePackrat()
        data.integer = pp.Word(pp.nums)
        data.op = pp.one_of("+ *")
        data.expr = pp.infix_notation(
            data.integer,
            [
                (data.op, 2, pp.opAssoc.LEFT, self.expr_action),
            ],
        )

    def compute(self, data):
        return sum(int(self.evaluate(data.expr, expr)) for expr in data.expressions)

    def evaluate(self, expr, text):
        self.interim = {}

        return expr.parse_string(text)[0]

    def expr_action(self, loc, toks):
        toks = toks[0]
        lhs = toks[0]
        txt = lhs

        for i in range(1, len(toks), 2):
            op = toks[i]
            rhs = toks[i + 1]
            lhs = str(eval(lhs + op + rhs))
            txt += op + rhs

        self.interim[txt] = str(lhs)
        result = int(lhs)
        return str(result)

    def example_input(self):
        return "1 + 2 * 3 + 4 * 5 + 6"

    def example_answer(self):
        return 71

    def tests(self):
        yield "2 * 3 + (4 * 5)", 26, "2 * 3 + (4 * 5) becomes 26."
        yield "5 + (8 * 3 + 9 + 3 * 4 * 3)", 437, "5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437."
        yield "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240, "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240."
        yield "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632, "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632."


class PartB(PartA):
    def config(self, data):
        data.expr = pp.infix_notation(
            data.integer,
            [
                ("+", 2, pp.opAssoc.LEFT, self.expr_action),
                ("*", 2, pp.opAssoc.LEFT, self.expr_action),
            ],
        )

    def example_answer(self):
        return 231

    def tests(self):
        yield "1 + (2 * 3) + (4 * (5 + 6))", 51, "1 + (2 * 3) + (4 * (5 + 6)) becomes 51."
        yield "2 * 3 + (4 * 5)", 46, "5 + 2 * 3 + (4 * 5) becomes 46."
        yield "5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445, "5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445."
        yield "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060, "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060."
        yield "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340, "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340."


Day.do_day(18, 2020, PartA, PartB)
