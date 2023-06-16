import sys
import timeit
import rich
from rich.console import Console
from aocd.models import Puzzle


def submit(puzzle: Puzzle, answer, value):
    console = Console()

    console.print()
    console.print("  >>", answer, ": ", value)
    if answer not in ("answer_a", "answer_b"):
        console.print("Answer ignored: answer does not match answer_a or answer_b")
        return

    if type(value) == int:
        value_str = str(value)
    elif type(value) == str:
        value_str = value
    else:
        console.print("Answer ignored: value type is neither int nor string")
        return

    if answer == "answer_a" and puzzle.answered_a:
        if value_str == puzzle.answer_a:
            console.print(f"  :white_check_mark:  [bold green]OK[/] (Already answered, values match)")
        else:
            console.print(f"  :x: [bold red]Fail[/] Value differs from previous: ", puzzle.answer_a)
        return

    if answer == "answer_b" and puzzle.answered_b:
        if value_str == puzzle.answer_b:
            console.print(f"  :white_check_mark: [bold green]OK[/] (Already answered, values match)")
        else:
            console.print(f"  :x: [bold red]Fail[/] Value differs from previous: ", puzzle.answer_b)
        return

    console.input("Submit answer? (y/n)")
    f = sys.stdin
    line = f.read(1)
    if line[0] == "y":
        setattr(puzzle, answer, value_str)
        console.print("Answer Submitted")


class Dump:
    pass


class Day:
    def __init__(self):
        self.console = Console()

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
        return ""

    def tests(self):
        return []

    def test_solve(self, test_text, config=None):
        data = Dump()
        data.config = config
        self.parse(test_text.strip("\n"), data)
        self.config(data)
        result = self.compute(data)
        return result

    def test(self, puzzle: Puzzle):
        self.console.print("Start test ...")
        t = timeit.default_timer()
        passed_tests = 0
        example_text = self.example_input()
        if example_text is None:
            example_text = puzzle.example_data
        tests = [(example_text, self.example_answer(), "Example")]
        tests.extend(self.tests())
        with self.console.status("Testing..."):
            for text, result_ok, *more in tests:
                passed = self.execute_test(text, result_ok, more)
                if passed:
                    passed_tests += 1
        self.console.print(f"Testing finished after {timeit.default_timer() - t:.2f}s")
        self.console.print(f"{passed_tests} of {len(tests)} passed")
        self.console.print("")
        return passed_tests == len(tests)

    def execute_test(self, text, result_ok, more):
        test_name = "" if len(more) == 0 else f"'{more[0]}'"
        result = self.test_solve(text)
        if result == result_ok or not result_ok:
            self.console.print(f"  :white_check_mark:  Test {test_name} [bold green]OK[/]  Result: {result}")
            return True
        else:
            self.console.print(f"  :x:  Test {test_name} [bold red]Failed[/]")
            self.console.print(f"  !! Expected {result_ok} but got {result}")
            return False

    def do_solve(self, puzzle_text):
        self.console.print("Starting to solve...")
        t = timeit.default_timer()
        data = Dump()
        data.config = None
        with self.console.status("Parse input..."):
            self.parse(puzzle_text, data)
        with self.console.status("Config..."):
            self.config(data)
        with self.console.status("Compute..."):
            result = self.compute(data)
        self.console.print(f"Finished solving after {timeit.default_timer() - t:.2f}s")
        return result

    def do_part(self, puzzle: Puzzle):
        self.console.rule(f"{self.answer_name()}", style="blue")
        if self.test(puzzle):
            text = puzzle.input_data
            result = self.do_solve(text)
            submit(puzzle, self.answer_name(), result)
        self.console.print()

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
