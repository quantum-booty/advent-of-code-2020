from collections import defaultdict
from typing import DefaultDict, List

# if the previous number is not called before, then the next number will be 0.
# The next number will be the difference in turns of when the previous number was last called.
# Need to remember what number are called and its position when it was last called.
# Use a dictionary to model this, use number as key, position as value.


def part1(input: List[int], turn_goal: int = 2020):
    last_seen: DefaultDict[int, int] = defaultdict(int)
    for turn, called in enumerate(input):
        last_seen[called] = turn + 1

    turn = len(input) + 1
    prev_called = 0
    # all_called = input + [0]
    while True:
        if last_seen[prev_called]:
            called = turn - last_seen[prev_called]
        else:
            called = 0

        last_seen[prev_called] = turn
        # all_called.append(called)
        turn += 1
        prev_called = called

        if turn == turn_goal:
            return (called)


test_input = [0, 3, 6]
assert part1(test_input) == 436

test_input = [1, 3, 2]
assert part1(test_input) == 1

input = [19, 20, 14, 0, 9, 1]
print(part1(input))

test_input = [0, 3, 6]
goal = 30000000
assert part1(test_input, goal) == 175594

print(part1(input, goal))
