from day_11_refactored import get_seats, all_rules, find_equilibrium, check, count_occupied, get_dims, get_pos, get_raw

test_raw_ayaya = """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#....."""
# seats = get_seats(test_raw_ayaya)
# print(seats)
# width, height = get_dims(test_raw_ayaya)
# count = count_adjacent(seats, 4, 3, True, height, width)
# print(count)
# assert count_adjacent(seats, 4, 3, True, height, width) == 8

test_raw_0 = """.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##."""
seats = get_seats(test_raw_0)
width, height = get_dims(test_raw_0)
assert check(seats, 3, 3, True, height, width) == 0
assert check(seats, 0, 1, True, height, width) == 4
assert check(seats, 1, 2, True, height, width) == 7

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

test_raw_2 = """#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#"""

test_raw_3 = """#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#"""

test_raw_4 = """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#"""

test_raw_5 = """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#"""

test_raw_6 = """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#"""

test_raw_7 = """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#"""

# %%
seats = get_seats(test_raw)
height, width = get_dims(test_raw)
seats = all_rules(seats, 5, True, height, width)
assert seats == get_seats(test_raw_1)

seats = all_rules(seats, 5, True, height, width)
assert seats == get_seats(test_raw_2)

seats = all_rules(seats, 5, True, height, width)
assert seats == get_seats(test_raw_3)

seats = all_rules(seats, 5, True, height, width)
assert seats == get_seats(test_raw_4)

seats = all_rules(seats, 5, True, height, width)
assert seats == get_seats(test_raw_5)

seats = all_rules(seats, 5, True, height, width)
assert seats == get_seats(test_raw_6)
# %%
seats = get_seats(test_raw)
seats = find_equilibrium(seats, 5, True, height, width)
print(count_occupied(seats))
assert count_occupied(seats) == 26
