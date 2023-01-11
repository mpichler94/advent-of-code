def read_input():
    file = open('day10/input.txt', encoding='utf8')
    data = file.read().splitlines()
    file.close()

    return data


def part_a(lines):
    score = 0
    for line in lines:
        characters = []
        for char in line:
            if is_opening(char):
                characters.append(char)
            elif len(characters) == 0:
                break
            elif not match_closing(characters.pop(), char):
                score += get_error_score(char)
                break

    print(f'syntax error score is {score}')


def is_opening(char):
    return char in ['(', '[', '{', '<']


def match_closing(opening, closing):
    if opening == '(' and closing == ')':
        return True
    if opening == '[' and closing == ']':
        return True
    if opening == '{' and closing == '}':
        return True
    if opening == '<' and closing == '>':
        return True


def get_error_score(char):
    match char:
        case ')': return 3
        case ']': return 57
        case '}': return 1197
        case '>': return 25137


def part_b(lines):
    scores = []
    for line in lines:
        characters = []
        corrupt = False
        for char in line:
            if is_opening(char):
                characters.append(char)
            elif len(characters) == 0:
                corrupt = True
                break
            elif not match_closing(characters.pop(), char):
                corrupt = True
                break

        if corrupt:
            continue

        score = 0
        characters.reverse()
        for char in characters:
            score *= 5
            score += get_completion_score(char)

        scores.append(score)

    scores.sort()

    print(f'middle completion score is {scores[len(scores) // 2]}')


def get_completion_score(char):
    match char:
        case '(': return 1
        case '[': return 2
        case '{': return 3
        case '<': return 4


def main():
    lines = read_input()
    part_a(lines)
    part_b(lines)


if __name__ == '__main__':
    main()
