from utils.aoc_base import Day
import copy


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.pairs = []
        for i in range(0, len(lines), 3):
            left_line = lines[i].strip()
            left = eval(left_line)

            right_line = lines[i+1].strip()
            right = eval(right_line)

            data.pairs.append([left, right])

    def compute(self, data):
        index_sum = 0
        indices = []
        for i, pair in enumerate(data.pairs):
            result, _ = self.check_order(pair[0], pair[1], i+1)
            if result:
                index_sum += (i + 1)
                indices.append(i+1)

        return index_sum

    def check_order(self, left, right, i, depth=0):
        while True:
            if type(left) == int:
                left = [left]
            if type(right) == int:
                right = [right]
            if len(left) == 0:
                if len(right) > 0:
                    return True, True
                else:
                    return True, False
            if len(right) == 0:
                return False, True

            current_left = left.pop(0)
            current_right = right.pop(0)

            if type(current_left) == list or type(current_right) == list:
                ret, imm = self.check_order(current_left, current_right, i, depth+1)
                if not ret:
                    return False, True
                if imm:
                    return ret, True

            else:
                if current_left < current_right:
                    return True, True
                if current_left > current_right:
                    return False, True

    def example_answer(self):
        return 13


class PartB(PartA):
    def compute(self, data):
        packets = [packet for packets in data.pairs for packet in packets]
        s_packets = [[[2]], [[6]]]

        for packet in packets:
            i = 0
            while i < len(s_packets):
                result, _ = self.check_order(copy.deepcopy(packet), copy.deepcopy(s_packets[i]), 0)
                if result:
                    break
                i += 1
            s_packets.insert(i, packet)

            index1 = s_packets.index([[2]]) + 1
            index2 = s_packets.index([[6]]) + 1

        return index1 * index2

    def example_answer(self):
        return 140


Day.do_day(13, 2022, PartA, PartB)
