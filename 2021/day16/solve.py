from utils.aoc_base import Day
from operator import mul
from functools import reduce


class Packet:
    def __init__(self, version, type, length, content) -> None:
        self.version = version
        self.type = type
        self.length = length
        self.content = content

    @classmethod
    def from_string(cls, text):
        version = int(text[:3], 2)
        packet_type = int(text[3:6], 2)
        content = text[6:]

        if packet_type == 4:   # literal packet
            length, content = cls.parse_literal(content)
        else:
            length, content = cls.parse_subpackets(content)

        return cls(version, packet_type, length + 6, content)

    @staticmethod
    def parse_literal(text):
        value = ''
        length = 0
        while True:
            value += text[1:5]
            length += 5
            if text[0] == '0':
                break
            text = text[5:]
        return length, int(value, 2)

    @staticmethod
    def parse_subpackets(text):
        length = 1
        subpackets = []
        length_type = text[0]

        if length_type == '0':
            subpacket_length = int(text[1:16], 2)
            length += 15
            text = text[16:]
        else:
            subpacket_length = int(text[1:12], 2)
            length += 11
            text = text[12:]

        current_length = 0
        while current_length < subpacket_length:
            subpacket = Packet.from_string(text)
            subpackets.append(subpacket)
            length += subpacket.length
            text = text[subpacket.length:]
            current_length += 1 if length_type == '1' else subpacket.length

        return length, subpackets

    def version_sum(self):
        if self.type == 4:
            return self.version
        return self.version + sum(sp.version_sum() for sp in self.content)

    def get_value(self):
        match self.type:
            case 0: return sum([sub.get_value() for sub in self.content])
            case 1: return reduce(mul, [sub.get_value() for sub in self.content], 1)
            case 2: return min([sub.get_value() for sub in self.content])
            case 3: return max([sub.get_value() for sub in self.content])
            case 4: return self.content
            case 5: return self.content[0].get_value() > self.content[1].get_value()
            case 6: return self.content[0].get_value() < self.content[1].get_value()
            case 7: return self.content[0].get_value() == self.content[1].get_value()
            case _: raise RuntimeError(f'Invalid packet type: {self.type}')

    def __repr__(self):
        if self.type == 4:
            return f'Packet(V{self.version} T{self.type} -> {self.content}'
        else:
            return f'Packet(V{self.version} T{self.type} [' + ''.join(sp.__repr__() for sp in self.content) + '])'


class PartA(Day):
    def parse(self, text, data):
        bin_data = ''.join(f'{int(char, 16):04b}' for char in text)
        data.packet = Packet.from_string(bin_data)

    def compute(self, data):
        return data.packet.version_sum()

    def example_answer(self):
        return 16

    def example_input(self):
        return '8A004A801A8002F478'

    def tests(self):
        yield '620080001611562C8802118E34', 12, 'Operator packet(v3) with 2 subpackets'
        yield 'C0015000016115A2E0802F182340', 23, 'Operator packet'
        yield 'A0016C880162017C3686B18A3D4780', 31, 'Multiple nested operator packets'


class PartB(PartA):
    def compute(self, data):
        return int(data.packet.get_value())

    def example_answer(self):
        return 15

    def tests(self):
        yield 'C200B40A82', 3, 'sum of 1 + 2'
        yield '04005AC33890', 54, 'product of 6 * 9'
        yield '880086C3E88112', 7, 'min of 7, 8, and 9'
        yield 'CE00C43D881120', 9, 'maximum of 7, 8, and 9'
        yield 'D8005AC2A8F0', 1, 'produces 1, because 5 is less than 15'
        yield 'F600BC2D8F', 0, 'produces 0, because 5 is not greater than 15'
        yield '9C005AC2F8F0', 0, 'produces 0, because 5 is not equal to 15'
        yield '9C0141080250320F1802104A08', 1, 'produces 1, because 1 + 3 = 2 * 2'


Day.do_day(16, 2021, PartA, PartB)
