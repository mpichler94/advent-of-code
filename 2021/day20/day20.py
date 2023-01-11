import numpy as np
from tqdm import tqdm


def read_input():
    file = open('day20/input.txt', encoding='utf8')
    data = file.read().splitlines()
    file.close()

    lut = []
    image = []

    for char in data[0]:
        lut.append(1 if char == '#' else 0)

    for i in range(2, len(data)):
        line = data[i]
        row = []
        for char in line:
            row.append(1 if char == '#' else 0)
        image.append(row)

    lut = np.array(lut, dtype=int)
    image = np.array(image, dtype=int)
    return lut, image


def get_window(image, c_x, c_y, background):
    window = np.full((3, 3), background, dtype=int)
    width, height = image.shape

    for y in range(c_y - 1, c_y + 2):
        for x in range(c_x - 1, c_x + 2):
            if y < 0 or y >= height or x < 0 or x >= width:
                continue
            window[y - c_y + 1, x - c_x + 1] = image[y, x]

    return window


def get_enhanced_value(lut, window):
    flattened = np.reshape(window, 9)
    index = 0
    for i in range(len(flattened)):
        index += flattened[i] << 8 - i
    return lut[index]


def enhance(lut, image,  background):
    width, height = image.shape
    new_image = np.zeros((width + 2, height + 2), dtype=int)
    for y in range(-1, height + 1):
        for x in range(-1, width + 1):
            w = get_window(image, x, y, background)
            v = get_enhanced_value(lut, w)
            new_image[y + 1, x + 1] = v

    return new_image


def part_a(lut, image):
    image = enhance(lut, image, 0)
    background = lut[0]
    image = enhance(lut, image, background)

    count = np.sum(image == 1)
    print(f'[a] number of lit pixels = {count}')


def part_b(lut, image):
    background = 0
    for i in tqdm(range(50)):
        image = enhance(lut, image, background)
        background = lut[0 if background == 0 else 1]

    count = np.sum(image == 1)
    print(f'[b] number of lit pixels = {count}')


def main():
    lut, image = read_input()
    part_a(lut, image)
    part_b(lut, image)


if __name__ == '__main__':
    main()
