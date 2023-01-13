from utils.aoc_base import Day


class PartA(Day):
    def parse(self, text, data):
        data.lines = text.splitlines()

    def compute(self, data):
        most_common = self.get_most_common(data.lines)
        gamma = self.bin_to_dec(most_common)
        epsilon = self.bin_to_dec(self.invert_bits(most_common))

        return gamma * epsilon

    @staticmethod
    def get_most_common(data):
        num_bits = len(data[0])
        one_bits = [0] * num_bits
        for number in data:
            for i in range(len(number)):
                if number[i] == '1':
                    one_bits[i] += 1

        num = len(data)
        most_common = ''
        for i in range(len(one_bits)):
            zero_bits = num - one_bits[i]
            if one_bits[i] > zero_bits:
                most_common += '1'
            elif one_bits[i] < zero_bits:
                most_common += '0'
            else:
                most_common += '1'

        return most_common

    @staticmethod
    def bin_to_dec(number):
        return int(number, base=2)

    @staticmethod
    def invert_bits(number):
        return ''.join('1' if number[i] == '0' else '0' for i in range(len(number)))

    def example_answer(self):
        return 198


class PartB(PartA):
    def compute(self, data):
        oxygen = self.get_oxygen(data.lines)
        oxygen = self.bin_to_dec(oxygen)

        co2 = self.get_co2(data.lines)
        co2 = self.bin_to_dec(co2)

        return oxygen * co2

    def get_oxygen(self, data):
        data = data.copy()
        for i in range(len(data[0])):
            data = self.get_most_common_numbers(data, i)

        return data[0]

    def get_most_common_numbers(self, data, i):
        most_common = self.get_most_common(data)
        return [number for number in data if number[i] == most_common[i]]

    def get_co2(self, data):
        data = data.copy()
        for i in range(len(data[0])):
            data = self.get_least_common_numbers(data, i)
            if len(data) == 1:
                break
        return data[0]

    def get_least_common_numbers(self, data, i):
        most_common = self.get_most_common(data)
        return [number for number in data if number[i] != most_common[i]]

    def example_answer(self):
        return 230


Day.do_day(3, 2021, PartA, PartB)
