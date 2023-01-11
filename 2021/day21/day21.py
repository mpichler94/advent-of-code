from functools import lru_cache

last_die_value = 0


def read_input():
    file = open('day21/example.txt', encoding='utf8')
    data = file.read().splitlines()
    file.close()

    pos1 = int(data[0][-1])
    pos2 = int(data[1][-1])
    return pos1, pos2


def roll_deterministic_die():
    global last_die_value
    last_die_value += 1
    return last_die_value


def get_rolls():
    return roll_deterministic_die() + roll_deterministic_die() + roll_deterministic_die()


def part_a(pos1, pos2):
    turn = 1
    score1 = 0
    score2 = 0

    while True:
        if turn % 2 == 1:
            pos1 = (pos1 + get_rolls() - 1) % 10 + 1
            score1 += pos1
            if score1 >= 1000:
                break
        else:
            pos2 = (pos2 + get_rolls() - 1) % 10 + 1
            score2 += pos2
            if score2 >= 1000:
                break
        turn += 1

    losing_score = min(score1, score2)
    num_rolls = turn * 3

    print(f'[a] losing score * num rolls = {losing_score * num_rolls}')


# possible 3 dice combinations: 1 * 3, 3 * 4, 6 * 5, 7 * 6, 6 * 7, 3 * 8, 1 * 9
rolls = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


@lru_cache(maxsize=None)    # caches inputs and outputs to skip repeating function calls
def roll_dirac(pos_a, pos_b, score_a, score_b):
    wins_a = 0
    wins_b = 0

    for roll, times in rolls.items():
        pos = (pos_a + roll - 1) % 10 + 1
        score = score_a + pos
        if score >= 21:
            wins_a += times
            continue
        tmp_b, tmp_a = roll_dirac(pos_b, pos, score_b, score)

        wins_a += tmp_a * times
        wins_b += tmp_b * times

    return wins_a, wins_b


def part_b(pos_1, pos_2):

    times_a, times_b = roll_dirac(pos_1, pos_2, 0, 0)
    if times_a > times_b:
        print(f'[b] Player 1 wins in {times_a} universes')
    else:
        print(f'[b] Player 2 wins in {times_b} universes')


def main():
    pos1, pos2 = read_input()
    part_a(pos1, pos2)
    part_b(pos1, pos2)


if __name__ == '__main__':
    main()
