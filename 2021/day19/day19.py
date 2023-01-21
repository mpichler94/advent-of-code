from utils.aoc_base import Day
import itertools
import numpy as np
from tqdm import tqdm


class PartA(Day):
    def parse(self, text, data):
        data.scanners = []
        scanner = []
        for line in text.splitlines():
            if line == "":
                continue
            if line.startswith("--- scanner"):
                if len(scanner) > 0:
                    data.scanners.append(np.array(scanner, dtype=np.int16))
                scanner = []
            else:
                coords = line.split(",")
                scanner.append([int(coords[0]), int(coords[1]), int(coords[2])])
        if len(scanner) > 0:
            data.scanners.append(np.array(scanner, dtype=np.int16))

    def compute(self, data):
        scanner0 = data.scanners.pop(0)
        i = 0
        count = 0
        data.positions = np.zeros((len(data.scanners), 3), dtype=np.int16)
        with tqdm(total=len(data.scanners)) as pbar:
            while len(data.scanners) > 0:
                matched, pos = self.match_scanner(scanner0, data.scanners[i])
                if matched is not None:
                    scanner0 = np.concatenate([scanner0, matched], dtype=np.int16)
                    scanner0 = np.unique(scanner0, axis=0)
                    data.positions[count] = pos
                    count += 1
                    data.scanners.pop(i)
                    pbar.update(1)
                    if len(data.scanners) == 0:
                        break
                    i %= len(data.scanners)
                else:
                    i = (i + 1) % len(data.scanners)

        return len(scanner0)

    def match_scanner(self, scanner0, scanner):
        indices = list(itertools.product(range(len(scanner0)), range(len(scanner))))

        for r in range(24):
            rotated = self.rotate(np.copy(scanner), r)
            for i in indices:
                delta = scanner0[i[0]] - rotated[i[1]]
                rotated += delta
                if self.count_overlaps(scanner0, rotated) > 11:
                    return rotated, delta

        return None, None

    @staticmethod
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
                scanner *= -1
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
                scanner *= -1
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
                scanner *= -1
            case 23:
                scanner[:, [1, 2, 0]] = scanner[:, [0, 1, 2]]
                scanner[:, [1, 2]] = -scanner[:, [1, 2]]

        return scanner

    @staticmethod
    def count_overlaps(scanner0, scanner):
        return np.sum((scanner0[:, None] == scanner).all(-1).any(-1))

    def example_answer(self):
        return 79

    def example_input(self):
        return """
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""


class PartB(PartA):
    def compute(self, data):
        PartA.compute(self, data)

        max_dist = 0
        for i in itertools.combinations(range(len(data.positions)), 2):
            dist = np.linalg.norm(data.positions[i[0]] - data.positions[i[1]], 1)
            if dist > max_dist:
                max_dist = dist
        return int(max_dist)

    def example_answer(self):
        return 3621


Day.do_day(19, 2021, PartA, PartB)
