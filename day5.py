# %%
from collections import namedtuple


def partition(low: int, up: int, upper: bool) -> tuple:
    if upper:
        low = int((up + low + 1) / 2)
    else:
        up = int((up + low - 1) / 2)
    return (low, up)


Seat = namedtuple('Seat', ["row", "column", "seatID"])


def find_seat(seat_str: str) -> Seat:
    # method 1
    upper_or_lower = [char == 'B' for char in seat_str[:7]]
    left_or_right = [char == 'R' for char in seat_str[7:10]]

    row_min, row_max = 0, 127
    for i in upper_or_lower:
        row_min, row_max = partition(row_min, row_max, i)
    assert row_min == row_max

    col_min, col_max = 0, 7
    for i in left_or_right:
        col_min, col_max = partition(col_min, col_max, i)
    assert col_min == col_max

    # method 2: converts binary to decimal
    row_min = int(''.join(['1' if char == 'B' else '0' for char in seat_str[:7]]), 2)
    col_min = int(''.join(['1' if char == 'R' else '0' for char in seat_str[7:10]]), 2)

    return Seat(row=row_min, column=col_min, seatID=row_min * 8 + col_min)


input = """BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
"""
# : row 70, column 7, seat ID 567.
# : row 14, column 7, seat ID 119.
# : row 102, column 4, seat ID 820

with open('inputs/5.txt', 'r') as file:
    input = file.read()
    # seats = [find_seat(seat_str) for seat_str in file]
    seats = [find_seat(seat_str) for seat_str in input.splitlines()]

print(max(seat.seatID for seat in seats))

# %% Method 1

import pandas as pd

x = pd.DataFrame(seats)

print()
y = x.groupby('row').sum().column != 28
print(y[y])
print(x[x.row == 79])
79 * 8 + 4

# %% Method 2

seat_ids = [seat.seatID for seat in seats]
lo = min(seat_ids)
hi = max(seat_ids)
print([x for x in range(lo, hi) if x not in seat_ids and x - 1 in seat_ids and x + 1 in seat_ids])
