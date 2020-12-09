from typing import List, Tuple
test_raw = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""


def get_input(raw: str) -> List[int]:
    return [int(num) for num in raw.splitlines()]


def find_product(inputs: List[int], goal: int) -> bool:
    # From day 1
    needs = {goal - i for i in inputs}
    found = False
    for i in inputs:
        if i in needs:
            found = True
            break
    return found


def find_invalid(input: List[int], preamble: int = 5) -> Tuple[int, int]:
    for i, num in enumerate(input):
        if i < preamble:
            continue
        window = input[i - preamble:i]
        if not find_product(window, num):
            invalid_num = num
            invalid_idx = i
    return invalid_idx, invalid_num


# part 1 test
test_input = get_input(test_raw)
preamble = 5
print('part 1 test', find_invalid(test_input, preamble)[0])

# part 1
with open('inputs/9.txt', 'r') as file:
    input = get_input(file.read())

preamble = 25
invalid_idx, invalid_num = find_invalid(input, preamble)
print('part 1', invalid_num)

# part 2


def find_encryp_weakness(input: List[int], invalid_idx: int, invalid_num: int) -> int:
    weakness = -1
    # This is brute force approach, I can alternatively add to previously
    # summed window to reduce computation.
    for win_max_idx in range(2, invalid_idx):
        for win_min_idx in range(invalid_idx - 2):
            window = input[win_min_idx:win_max_idx]
            if sum(window) == invalid_num:
                weakness = min(window) + max(window)
                break
    return weakness


print('part 2 test', find_encryp_weakness(test_input, *find_invalid(test_input, preamble=5)))
print('part 2', find_encryp_weakness(input, *find_invalid(input, preamble=25)))
