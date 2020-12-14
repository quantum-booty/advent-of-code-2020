from typing import Tuple, Optional, List
import re


def parse_line(line: str) -> Tuple[Optional[str], Optional[int], Optional[str]]:
    mask = None
    mem_loc = None
    val_bin = None

    # use re for the sake of practicing regex
    m = re.findall(r'(mask) = (.*)', line)
    if m:
        mask = m[0][1]
    mem_val = re.findall(r'\[(\d+)\] = (\d+)', line)
    if mem_val:
        mem_loc = int(mem_val[0][0])
        val = int(mem_val[0][1])
        val_bin = bin(val)[2:]
    return mask, mem_loc, val_bin


def apply_mask(val_bin: str, mask: str) -> str:
    new_val = ['0'] * (len(mask) - len(val_bin))
    new_val += list(val_bin)
    for i, m in enumerate(mask):
        if m != 'X':
            new_val[i] = m
    return ''.join(new_val)


def part1(raw: str) -> int:
    mask: str
    mems = {}
    for line in raw.splitlines():
        m, mem_loc, val_bin = parse_line(line)

        if m:
            mask = m
        if mem_loc and val_bin:
            val = int(apply_mask(val_bin, mask), 2)
            mems[mem_loc] = val
    return sum(mems.values())


def float_mask(mask: str) -> List[str]:
    positions = [i for i, char in enumerate(mask) if char == 'X']
    count = mask.count('X')
    masks = []
    for i in range(2**count):
        m = bin(i)[2:]
        m = '0' * (count - len(m)) + m
        # Replace 0 with z so they are not skipped in apply_mask_2
        m = m.replace('0', 'z')

        new_mask = list(mask)
        for pos, char in enumerate(m):
            new_mask[positions[pos]] = char
        masks.append(''.join(new_mask))
    return masks


def apply_mask_2(mem_loc_bin: str, mask: str) -> str:
    new_mem_loc_bin = ['0'] * (len(mask) - len(mem_loc_bin))
    new_mem_loc_bin += list(mem_loc_bin)
    for i, m in enumerate(mask):
        if m == '0':
            # if 0 unchanged
            continue
        new_mem_loc_bin[i] = m
    return ''.join(new_mem_loc_bin)


def part2(raw: str) -> int:
    # if 0 unchanged
    # if 1 change to 1
    # if X -> floating bit -> all combinations
    mems = {}
    for line in raw.splitlines():
        m, mem_loc, val_bin = parse_line(line)
        if m:
            masks = float_mask(m)

        if mem_loc and val_bin:
            mem_loc_bin = bin(mem_loc)[2:]
            for mask in masks:
                mem_loc = int(apply_mask_2(mem_loc_bin, mask).replace('z', '0'), 2)
                mems[mem_loc] = int(val_bin, 2)
    return sum(mems.values())


test_raw = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

assert part1(test_raw) == 165

test_raw_2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

assert part2(test_raw_2) == 208

with open('inputs/14.txt', 'r') as file:
    raw = file.read()

    print(part1(raw))
    print(part2(raw))
