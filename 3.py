from collections import namedtuple
raw = """0011000000010001000100010000100100010100010101000110010001011000000101010000101000000001101100010001000110000101001000101"""

width = 11
trees_tot = 0
for y in range(1, width):
    x = y * 3 % width

    pos = y * width + x

    trees_tot += int(raw[pos])

print(trees_tot)

# %%

with open('inputs/3.txt', 'r') as file:
    raw = file.read().replace('\n', '').replace('.', '0').replace('#', '1')

width = 31

right = [1, 3, 5, 7, 1]
down = [1, 1, 1, 1, 2]
trees_mult = 1
for slope in range(5):
    trees_tot = 0
    for y in range(1, 323, down[slope]):
        x = y * right[slope] % width

        pos = y * width + x

        trees_tot += int(raw[pos])
    trees_mult *= trees_tot

print(trees_mult)
