from day_11 import *

test_raw = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

test_raw_1 = """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##"""

test_raw_2 = """#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##"""

test_raw_3 = """#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##"""

# %%

seats = get_seats(test_raw)
width, height = get_dims(seats)

seats = first_rule(seats)
assert get_raw(seats) == test_raw_1

assert count_adjacent(seats, 0, 0) == 2
assert count_adjacent(seats, height - 1, width - 1) == 2
assert count_adjacent(seats, height - 1, 0) == 1
assert count_adjacent(seats, 0, 3) == 4

assert get_raw(second_rule(seats)) == test_raw_2

# %%

seats = get_seats(test_raw)
seats = find_equilibrium(seats)
assert count_occupied(seats) == 37
