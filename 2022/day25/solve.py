import math

import numpy as np

from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.snafu = text.splitlines()

    def compute(self, data):
        sum = 0

        for line in data.snafu:
            dec = self.snafu_to_decimal(line)
            sum += dec

        return self.decimal_to_snafu(sum)

    @staticmethod
    def snafu_to_decimal(snafu: str):
        dec = 0
        for i, char in enumerate(snafu):
            mul = 5 ** (len(snafu) - i - 1)

            match char:
                case '0':
                    continue
                case '1':
                    dec += mul
                case '2':
                    dec += 2 * mul
                case '-':
                    dec -= mul
                case '=':
                    dec -= 2 * mul

        return dec

    @staticmethod
    def decimal_to_snafu(decimal: int):
        snafu = []
        div = decimal
        fac = 0
        while abs(div) >= 5:
            div = math.trunc(div / 5)
            fac += 1

        while True:
            div = math.trunc(decimal / (5**fac))

            snafu.append(div)
            decimal -= div * 5**fac

            new_fac = fac - 1
            if abs(div) > 2:
                last_index = len(snafu)-1
                for i in range(last_index, -1, -1):
                    if abs(snafu[i]) > 2:
                        decimal += snafu[i] * 5**(last_index-i+fac)
                        sign = np.sign(snafu[i])
                        snafu.pop(-1)
                        new_fac += 1

                        if i > 0:
                            snafu[i-1] += sign
                            decimal -= sign * 5**(last_index-i+1+fac)
                        else:
                            snafu.insert(0, sign)
                            decimal -= sign * 5**(last_index+1+fac)

            if decimal == 0 and fac == 0:
                break

            fac = new_fac

        result = ''
        for digit in snafu:
            match digit:
                case 0:
                    result += '0'
                case 1:
                    result += '1'
                case 2:
                    result += '2'
                case -1:
                    result += '-'
                case -2:
                    result += '='
        return result

    def example_answer(self):
        return '2=-1=0'


class PartB(PartA):
    pass


Day.do_day(25, 2022, PartA, PartB)
