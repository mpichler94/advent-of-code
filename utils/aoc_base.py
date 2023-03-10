import sys
import timeit
from aocd.models import Puzzle


def submit(puzzle: Puzzle, answer, value):
    green = "\033[0;32m"
    red = "\033[0;31m"
    default = "\033[00m"

    print()
    print("  >>", answer, ": ", value)
    if answer not in ("answer_a", "answer_b"):
        print("Answer ignored: answer does not match answer_a or answer_b")
        return

    if type(value) == int:
        value_str = str(value)
    elif type(value) == str:
        value_str = value
    else:
        print("Answer ignored: value type is neither int nor string")
        return

    if answer == "answer_a" and puzzle.answered_a:
        if value_str == puzzle.answer_a:
            print(f"{green}  >> Ok {default}(Already answered, values match)")
        else:
            print(f"{red}  >> Fail {default}Value differs from previous: ", puzzle.answer_a)
        return


    if answer == "answer_b" and puzzle.answered_b:
        if value_str == puzzle.answer_b:
            print(f"{green}  >> Ok {default}(Already answered, values match)")
        else:
            print(f"{red}  >> Fail {default}Value differs from previous: ", puzzle.answer_b)
        return

    print("Submit answer? (y/n)")
    f = sys.stdin
    line = f.read(1)
    if line[0] == "y":
        setattr(puzzle, answer, value_str)
        print("Answer Submitted")


class Dump:
    pass

class Day:

    def answer_name(self):
        part = type(self).__name__[:5]
        if part not in ("PartA", "PartB"):
            raise RuntimeError("Class name must start with PartA or PartB")
        return "answer_" + part[-1].lower()


    def parse(self, text, data):
        data.text = text


    def config(self, data):
        pass


    def compute(self, data):
        return ''


    def tests(self):
        return []

    def test_solve(self, test_text, config=None):
        data = Dump()
        data.config = config
        self.parse(test_text.strip('\n'), data)
        self.config(data)
        result = self.compute(data)
        return result


    def test(self, puzzle: Puzzle):
        print('Start test ...')
        t = timeit.default_timer()
        passed_tests = 0
        example_text = self.example_input()
        if example_text is None:
            example_text = puzzle.example_data
        tests = [(example_text, self.example_answer(), "Example")]
        tests.extend(self.tests())
        for text, result_ok, *more in tests:
            passed = self.execute_test(text, result_ok, more)
            if passed:
                passed_tests += 1
        print(f"Testing finished after {timeit.default_timer() - t:.2f}s")
        print(f"{passed_tests} of {len(tests)} passed")
        print("")
        return passed_tests == len(tests)

    def execute_test(self, text, result_ok, more):
        green = "\033[0;32m"
        red = "\033[0;31m"
        default = "\033[00m"
        test_name = "" if len(more) == 0 else f"'{more[0]}'"
        result = self.test_solve(text)
        if result == result_ok or not result_ok:
            print(f"  {green}>>{default} Test {test_name} {green}OK{default}  Result: {result}")
            return True
        else:
            print(f"  {red}>>{default}  Test {test_name} {red}Failed{default}")
            print(f"  !! Expected {result_ok} but got {result}")
            return False

    def do_solve(self, puzzle_text):
        print("Starting to solve...")
        t = timeit.default_timer()
        data = Dump()
        data.config = None
        print("Parse input")
        self.parse(puzzle_text, data)
        print("Config")
        self.config(data)
        print("Compute")
        result = self.compute(data)
        print(f"Finished solving after {timeit.default_timer() - t:.2f}s")
        return result

    def do_part(self, puzzle: Puzzle):
        print(f"-------------------- starting {self.answer_name()} --------------------")
        if self.test(puzzle):
            text = puzzle.input_data
            result = self.do_solve(text)
            submit(puzzle, self.answer_name(), result)
        print()

    def example_answer(self):
        return None

    def example_input(self):
        return None

    @staticmethod
    def do_day(day, year, part_a, part_b):
        puzzle = Puzzle(day=day, year=year)
        if part_a is not None:
            part_a().do_part(puzzle)
        if part_b is not None:
            part_b().do_part(puzzle)
