import re

from utils.aoc_base import Day


class Passport:
    def __init__(self, byr, iyr, eyr, hgt, hcl, ecl, pid):
        self.data = [byr, iyr, eyr, hgt, hcl, ecl, pid]

    @classmethod
    def from_text(cls, text: str):
        text = text.replace("\n", " ")
        parts = text.split()
        data = {}
        for part in parts:
            key, value = part.split(":")
            data[key] = value
        return cls(
            data.get("byr"),
            data.get("iyr"),
            data.get("eyr"),
            data.get("hgt"),
            data.get("hcl"),
            data.get("ecl"),
            data.get("pid"),
        )

    def valid_a(self):
        for field in self.data:
            if field is None:
                return False
        return True

    def valid_b(self):
        if not self.valid_a():
            return False

        if self.data[0] is None or not self.data[0].isdigit():
            return False
        byr = int(self.data[0])
        if byr < 1920 or byr > 2002:
            return False

        if self.data[1] is None or not self.data[1].isdigit():
            return False
        iyr = int(self.data[1])
        if iyr < 2010 or iyr > 2020:
            return False

        if self.data[2] is None or not self.data[2].isdigit():
            return False
        eyr = int(self.data[2])
        if eyr < 2020 or eyr > 2030:
            return False

        idx = self.data[3].find("cm")
        if idx > 0:
            hgt = int(self.data[3][:-2])
            if hgt < 150 or hgt > 193:
                return False
        else:
            idx = self.data[3].find("in")
            if idx > 0:
                hgt = int(self.data[3][:-2])
                if hgt < 59 or hgt > 76:
                    return False
            else:
                return False

        if not re.match(r"^#[0-9a-f]{6}$", self.data[4]):
            return False

        if self.data[5] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            return False

        if not re.match(r"^\d{9}$", self.data[6]):
            return False

        return True


class PartA(Day):
    def parse(self, text, data):
        passports = text.split("\n\n")

        data.passports = []
        for passport in passports:
            data.passports.append(Passport.from_text(passport))

    def compute(self, data):
        return sum(passport.valid_a() for passport in data.passports)


class PartB(PartA):
    def compute(self, data):
        return sum(passport.valid_b() for passport in data.passports)


Day.do_day(4, 2020, PartA, PartB)
