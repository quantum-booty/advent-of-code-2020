from collections import defaultdict
from typing import DefaultDict, Iterator, List
import itertools

# if the previous number is not called before, then the next number will be 0.
# The next number will be the difference in turns of when the previous number was last called.
# Need to remember what number are called and its position when it was last called.
# Use a dictionary to model this, use number as key, position as value.


def play_game(starting_nums: List[int]) -> Iterator[int]:
    # Trying out the concept of generator/iterator from Joel Grus.
    last_seen: DefaultDict[int, int] = defaultdict(int)
    for turn, called in enumerate(starting_nums):
        last_seen[called] = turn + 1

    turn = len(starting_nums) + 1
    prev_called = 0
    # all_called = input + [0]
    for turn in itertools.count(len(starting_nums) + 1):
        if last_seen[prev_called]:
            called = turn - last_seen[prev_called]
        else:
            called = 0

        last_seen[prev_called] = turn
        # all_called.append(called)
        # turn += 1
        prev_called = called
        yield called


def get_nth_call(starting_nums, n=2020):
    game = play_game(starting_nums)
    for _ in range(n - len(starting_nums) - 1):
        n = next(game)

    return n


test_starting_numing_num = [0, 3, 6]
assert get_nth_call(test_starting_numing_num) == 436

test_starting_numing_num = [1, 3, 2]
assert get_nth_call(test_starting_numing_num) == 1

starting_num = [19, 20, 14, 0, 9, 1]
print(get_nth_call(starting_num))

test_starting_numing_num = [0, 3, 6]
goal = 30000000
assert get_nth_call(test_starting_numing_num, goal) == 175594

print(get_nth_call(starting_num, goal))
