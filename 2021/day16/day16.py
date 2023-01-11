from operator import mul
from functools import reduce


class Packet:
    def __init__(self, version, type, length, value, subpackets) -> None:
        self.version = version
        self.type = type
        self.length = length
        self.value = value
        self.subpackets = subpackets


def read_input():
    file = open('day16/input.txt', encoding='utf8')
    data = file.read()
    file.close()

    bin_data = f'{int(data, 16):b}'

    digits = []
    for char in bin_data:
        digits.append(int(char))

    return digits


def get_version(data):
    return to_dec(data[0:3])


def get_type(data):
    return to_dec(data[3:6])


def get_groups(data):
    packets = []
    pos = 6
    while True:
        packet = get_group(data, pos)
        packets.append(packet[1:])
        pos += 5
        if packet[0] == 0:  # last group
            break

    return packets


def get_group(data, pos):
    packet = data[pos:pos + 5]
    return packet


def get_sub_packets(data):
    read_packet(data)


def read_packet(data):
    version = get_version(data)
    packet_type = get_type(data)
    length = 6
    subpackets = []
    value = None

    if packet_type == 4:   # literal value
        groups = get_groups(data)
        value = get_literal_value(groups)
        length += len(groups) * 5
    else:
        length_type = data[6]
        if length_type == 1:    # 11 bits for num subpackets
            num_packets = to_dec(data[7:7 + 11])
            length += 12
            for _ in range(num_packets):
                subpacket = read_packet(data[length:])
                length += subpacket.length
                subpackets.append(subpacket)
        else:
            subpackets_length = to_dec(data[7:7 + 15])
            length += 16
            while subpackets_length > 0:
                subpacket = read_packet(data[length:])
                length += subpacket.length
                subpackets_length -= subpacket.length
                subpackets.append(subpacket)

    return Packet(version, packet_type, length, value, subpackets)


def to_dec(data):
    number = 0
    for i in range(len(data)):
        if data[i] == 1:
            number += 1 << (len(data) - i - 1)

    return number


def get_literal_value(groups):
    bits = []
    for group in groups:
        bits += group
    return to_dec(bits)


def sum_versions(packet):
    version_sum = packet.version
    for sub in packet.subpackets:
        version_sum += sum_versions(sub)

    return version_sum


def get_value(packet):
    sub_values = [get_value(sub) for sub in packet.subpackets]
    match packet.type:
        case 0:
            return sum(sub_values)
        case 1:
            return reduce(mul, sub_values, 1)
        case 2:
            return min(sub_values)
        case 3:
            return max(sub_values)
        case 4:
            return packet.value
        case 5:
            return get_value(packet.subpackets[0]) > get_value(packet.subpackets[1])
        case 6:
            return get_value(packet.subpackets[0]) < get_value(packet.subpackets[1])
        case 7:
            return get_value(packet.subpackets[0]) == get_value(packet.subpackets[1])
        case _:
            return 0


def part_a(data):
    packet = read_packet(data)
    version_sum = sum_versions(packet)

    print(f'[a] sum of version numbers = {version_sum}')


def part_b(data):
    packet = read_packet(data)
    value = get_value(packet)
    print(f'[b] value = {value}')


def main():
    matrix = read_input()
    part_a(matrix)
    part_b(matrix)


if __name__ == '__main__':
    main()
