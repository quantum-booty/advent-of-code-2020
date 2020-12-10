from typing import List, Deque
from collections import deque
from numba import jit


@jit(nopython=True)
def get_input(raw: str) -> List[int]:
    return [int(num) for num in raw.splitlines()]


@jit(nopython=True)
def find_product(numbers: Deque[int], goal: int) -> bool:
    # From day 1
    found = False
    needs = {goal - i for i in numbers}
    for i in numbers:
        if i in needs:
            found = True
            break
    return found


@jit(nopython=True)
def find_invalid(input: List[int], preamble: int = 5) -> int:
    # use deque for faster append and pop at the endpoints of window.
    window = deque()
    for i, num in enumerate(input):
        if i < preamble:
            window.append(num)
            continue
        if not find_product(window, num):
            invalid_num = num
            break
        window.append(num)
        window.popleft()
    return invalid_num


# part 2


@jit(nopython=True)
def find_encryp_weakness(input: List[int], invalid_num: int) -> int:
    for i, head in enumerate(input):
        j = i
        total = head
        while total < invalid_num and j < len(input):
            j += 1
            total += input[j]
        if total == invalid_num:
            slice = input[i:j + 1]
            return min(slice) + max(slice)


#
# Unit Tests
#

TEST_RAW = """35
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
576"""

TEST_INPUT = get_input(TEST_RAW)

invalid_num = find_invalid(TEST_INPUT, preamble=5)
assert invalid_num == 127
assert find_encryp_weakness(TEST_INPUT, invalid_num) == 62

#
# Problem
#

with open('inputs/9.txt', 'r') as file:
    input = get_input(file.read())

invalid_num = find_invalid(input, preamble=25)
print(invalid_num)
print(find_encryp_weakness(input, invalid_num))
