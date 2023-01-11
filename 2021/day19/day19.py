import itertools
import numpy as np
from tqdm import tqdm


def read_input():
    file = open('day19/input.txt', encoding='utf8')
    data = file.read().splitlines()
    file.close()

    scanners = []
    scanner = []
    for line in data:
        if line == '':
            continue
        if line.startswith('--- scanner'):
            if len(scanner) > 0:
                scanners.append(np.array(scanner))
            scanner = []
        else:
            coords = line.split(',')
            scanner.append([int(coords[0]), int(coords[1]), int(coords[2])])
    if len(scanner) > 0:
        scanners.append(np.array(scanner))

    return scanners


def translate(scanner, delta):
    scanner += delta
    return scanner


def rotate(scanner, rotation):
    match rotation:
        case 1:
            scanner[:, [2, 1]] = scanner[:, [1, 2]]
            scanner[:, 1] = -scanner[:, 1]
        case 2:
            scanner[:, [1, 2]] = -scanner[:, [1, 2]]
        case 3:
            scanner[:, [2, 1]] = scanner[:, [1, 2]]
            scanner[:, 2] = -scanner[:, 2]
        case 4:
            scanner[:, [0, 1]] = -scanner[:, [0, 1]]
        case 5:
            scanner[:, [2, 1]] = scanner[:, [1, 2]]
            scanner = -scanner
        case 6:
            scanner[:, [0, 2]] = -scanner[:, [0, 2]]
        case 7:
            scanner[:, [2, 1]] = scanner[:, [1, 2]]
            scanner[:, 0] = -scanner[:, 0]
        case 8:
            scanner[:, [2, 0, 1]] = scanner[:, [0, 1, 2]]
            scanner[:, [0, 2]] = -scanner[:, [0, 2]]
        case 9:
            scanner[:, [1, 0]] = scanner[:, [0, 1]]
            scanner[:, 2] = -scanner[:, 2]
        case 10:
            scanner[:, [2, 0, 1]] = scanner[:, [0, 1, 2]]
        case 11:
            scanner[:, [1, 0]] = scanner[:, [0, 1]]
            scanner[:, 0] = -scanner[:, 0]
        case 12:
            scanner[:, [2, 0, 1]] = scanner[:, [0, 1, 2]]
            scanner[:, [1, 2]] = -scanner[:, [1, 2]]
        case 13:
            scanner[:, [1, 0]] = scanner[:, [0, 1]]
            scanner[:, 1] = -scanner[:, 1]
        case 14:
            scanner[:, [2, 0, 1]] = scanner[:, [0, 1, 2]]
            scanner[:, [0, 1]] = -scanner[:, [0, 1]]
        case 15:
            scanner[:, [1, 0]] = scanner[:, [0, 1]]
            scanner = -scanner
        case 16:
            scanner[:, [1, 2, 0]] = scanner[:, [0, 1, 2]]
            scanner[:, [0, 1]] = -scanner[:, [0, 1]]
        case 17:
            scanner[:, [2, 0]] = scanner[:, [0, 2]]
            scanner[:, 1] = -scanner[:, 1]
        case 18:
            scanner[:, [1, 2, 0]] = scanner[:, [0, 1, 2]]
        case 19:
            scanner[:, [2, 0]] = scanner[:, [0, 2]]
            scanner[:, 0] = -scanner[:, 0]
        case 20:
            scanner[:, [2, 0]] = scanner[:, [0, 2]]
            scanner[:, 2] = -scanner[:, 2]
        case 21:
            scanner[:, [1, 2, 0]] = scanner[:, [0, 1, 2]]
            scanner[:, [0, 2]] = -scanner[:, [0, 2]]
        case 22:
            scanner[:, [2, 0]] = scanner[:, [0, 2]]
            scanner = -scanner
        case 23:
            scanner[:, [1, 2, 0]] = scanner[:, [0, 1, 2]]
            scanner[:, [1, 2]] = -scanner[:, [1, 2]]

    return scanner


def count_overlaps(scanner0, scanner):
    count2 = np.sum((scanner0[:, None] == scanner).all(-1).any(-1))

    return count2


def match_scanner(scanner0, scanner):
    indices = list(itertools.product(range(len(scanner0)), range(len(scanner))))

    for r in range(24):
        rotated = rotate(np.copy(scanner), r)
        for i in indices:
            delta = scanner0[i[0]] - rotated[i[1]]
            translated = translate(np.copy(rotated), delta)
            if count_overlaps(scanner0, translated) > 11:
                return translated, delta

    return None, None


def compute_distances(scanner):
    indices = itertools.combinations(range(len(scanner)), 2)
    distances = []
    for i in indices:
        dist = scanner[i[0]] - scanner[i[1]]
        dist = np.linalg.norm(dist)
        distances.append(dist)
    return np.array(distances)


def compare_distances(scanner1, scanner2):
    matches = scanner1.intersection(scanner2)
    if len(matches) < 12:
        return None
    i1 = scanner1.index(matches[0])
    i2 = scanner2.index(matches[0])
    return i1, i2


def find_matches(scanners):
    distances = []
    for scanner in scanners:
        distances.append(compute_distances(scanner))

    for i in itertools.combinations(range(len(distances)), 2):
        idx1, idx2 = compare_distances(distances[i[0]], distances[i[1]])
        if idx1 is None:
            continue
        translation = scanners[idx1] - scanner[idx2]

def part_a(scanners):
    scanner0 = scanners.pop(0)
    i = 0
    count = 0
    positions = np.zeros((len(scanners), 3))
    with tqdm(total=len(scanners)) as pbar:
        while len(scanners) > 0:
            matched, pos = match_scanner(scanner0, scanners[i])
            if matched is not None:
                scanner0 = np.concatenate([scanner0, matched])
                scanner0 = np.unique(scanner0, axis=0)
                positions[count] = pos
                count += 1
                scanners.pop(i)
                pbar.update(1)
                if len(scanners) == 0:
                    break
                i %= len(scanners)
            else:
                i = (i + 1) % len(scanners)

    print(f'[a] number of unique beacons = {len(scanner0)}')

    max_dist = 0
    for i in itertools.combinations(range(len(positions)), 2):
        dist = np.linalg.norm(positions[i[0]] - positions[i[1]], 1)
        if dist > max_dist:
            max_dist = dist

    print(f'[b] max distance = {max_dist}')


def main():
    scanners = read_input()
    part_a(scanners)


if __name__ == '__main__':
    main()
