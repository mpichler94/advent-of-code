from utils.aoc_base import Day
from collections import namedtuple


class File:
    def __init__(self, name, size=0, parent=None):
        self.name = name
        self.size = size
        self.parent = parent
        self.files = []

    def add_file(self, file):
        self.files.append(file)

    def file(self, name):
        for file in self.files:
            if file.name == name:
                return file

    def total_size(self):
        size = self.size
        size += sum(file.total_size() for file in self.files)
        return size


Command = namedtuple('Command', ['command', 'output'])


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        commands = []
        command = None
        output = []
        for line in lines:
            if line.startswith('$'):
                if command is not None:
                    commands.append(Command(command, output))
                    output = []
                command = line[2:]
            else:
                output.append(line)

        commands.append(Command(command, output))
        data.commands = commands[1:]

    def config(self, data):
        root = File("/")
        current_dir = root
        for command in data.commands:
            if command.command.startswith('ls'):
                for line in command.output:
                    if line.startswith('dir'):
                        current_dir.add_file(File(line[4:], parent=current_dir))
                    else:
                        parts = line.split()
                        current_dir.add_file(File(parts[1], int(parts[0]), current_dir))
            else:
                if command.command.endswith('..'):
                    current_dir = current_dir.parent
                else:
                    dest = command.command.split()[1]
                    current_dir = current_dir.file(dest)

        data.tree = root

    def compute(self, data):
        size = self.sum_sizes(data.tree)
        return size

    def sum_sizes(self, dir):
        dir_size = dir.total_size()
        size = 0
        if dir_size < 100000 and dir.size == 0:
            size += dir_size

        size += sum(self.sum_sizes(file) for file in dir.files)

        return size

    def example_input(self):
        return '''
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''

    def example_answer(self):
        return 95437


class PartB(PartA):
    def compute(self, data):
        needed = 30000000 - (70000000 - data.tree.total_size())
        min_size, min_dir = self.get_min_dir(data.tree, needed)

        return min_size

    def get_min_dir(self, dir, needed):
        min_size = dir.total_size()
        min_dir = dir

        for file in dir.files:
            child_min_size, child_min_dir = self.get_min_dir(file, needed)
            if needed < child_min_size <= min_size:
                min_dir = child_min_dir
                min_size = child_min_size

        return min_size, min_dir

    def example_answer(self):
        return 24933642


Day.do_day(7, 2022, PartA, PartB)
