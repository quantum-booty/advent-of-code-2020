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


def find_product(inputs: List[int], needed_sum: int) -> bool:
    needs = {needed_sum - i for i in inputs}
    found = False
    for i in inputs:
        if i in needs:
            # num = i
            found = True
            break
    # return num * (needed_sum - num)
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


preamble = 5
# part 1 test
test_input = get_input(test_raw)
print('part 1 test', find_invalid(test_input, preamble)[0])

# part 1
with open('inputs/9.txt', 'r') as file:
    input = get_input(file.read())

preamble = 25
invalid_idx, invalid_num = find_invalid(input, preamble)
print('part 1', invalid_num)

# part 2
input = test_input
invalid_idx, invalid_num = find_invalid(input, preamble=5)
for win_min_idx in range(invalid_idx - 2):
    for win_max_idx in range(2, invalid_idx):
        window = input[win_min_idx:win_max_idx]
        print(win_min_idx, win_max_idx, window)
        if sum(window) == invalid_num:
            print(window)
            print(min(window) + max(window))
        break
