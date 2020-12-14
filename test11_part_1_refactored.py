from day_11_refactored import get_seats, get_dims, check, all_rules, find_equilibrium, count_occupied

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

width, height = get_dims(test_raw)
seats = get_seats(test_raw)

seats = all_rules(seats, 4, False, height, width)
print(seats)
assert seats == get_seats(test_raw_1)

assert check(seats, 0, 0, False, height, width) == 2
assert check(seats, height - 1, width - 1, False, height, width) == 2
assert check(seats, height - 1, 0, False, height, width) == 1
assert check(seats, 0, 3, False, height, width) == 4

seats = all_rules(seats, 4, False, height, width)
print(seats)
assert seats == get_seats(test_raw_2)

# %%

seats = get_seats(test_raw)
seats = find_equilibrium(seats, 4, False, height, width)
assert count_occupied(seats) == 37
