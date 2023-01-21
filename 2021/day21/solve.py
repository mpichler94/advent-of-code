from utils.aoc_base import Day
from functools import lru_cache


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()

        data.pos1 = int(lines[0][-1])
        data.pos2 = int(lines[1][-1])
        self.last_die_value = 0

    def get_rolls(self):
        return self.roll_deterministic_die() + self.roll_deterministic_die() + self.roll_deterministic_die()

    def roll_deterministic_die(self):
        self.last_die_value += 1
        return self.last_die_value

    def compute(self, data):
        turn = 1
        score1 = 0
        score2 = 0

        while True:
            if turn % 2 == 1:
                data.pos1 = (data.pos1 + self.get_rolls() - 1) % 10 + 1
                score1 += data.pos1
                if score1 >= 1000:
                    break
            else:
                data.pos2 = (data.pos2 + self.get_rolls() - 1) % 10 + 1
                score2 += data.pos2
                if score2 >= 1000:
                    break
            turn += 1

        losing_score = min(score1, score2)
        num_rolls = turn * 3
        return losing_score * num_rolls

    def example_answer(self):
        return 739785


class PartB(PartA):
    def compute(self, data):
        times_a, times_b = self.roll_dirac(data.pos1, data.pos2, 0, 0)
        return max(times_a, times_b)

    @lru_cache(maxsize=None)    # caches inputs and outputs to skip repeating function calls
    def roll_dirac(self, pos_a, pos_b, score_a, score_b):
        # possible 3 dice combinations: 1 * 3, 3 * 4, 6 * 5, 7 * 6, 6 * 7, 3 * 8, 1 * 9
        rolls = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
        wins_a = 0
        wins_b = 0

        for roll, times in rolls.items():
            pos = (pos_a + roll - 1) % 10 + 1
            score = score_a + pos
            if score >= 21:
                wins_a += times
                continue
            tmp_b, tmp_a = self.roll_dirac(pos_b, pos, score_b, score)

            wins_a += tmp_a * times
            wins_b += tmp_b * times

        return wins_a, wins_b

    def example_answer(self):
        return 444356092776315


Day.do_day(21, 2021, PartA, PartB)
