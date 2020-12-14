from day_11 import get_seats, all_rules, find_equilibrium, count_adjacent, count_occupied, get_raw

test_raw_ayaya = """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#....."""
seats = get_seats(test_raw_ayaya)
assert count_adjacent(seats, 4, 3, True) == 8

test_raw_0 = """.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##."""
seats = get_seats(test_raw_0)
assert count_adjacent(seats, 3, 3, True) == 0
assert count_adjacent(seats, 0, 1, True) == 4
assert count_adjacent(seats, 1, 2, True) == 7

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
seats = all_rules(seats, 5, True)
assert get_raw(seats) == test_raw_1

seats = all_rules(seats, 5, True)
assert get_raw(seats) == test_raw_2

seats = all_rules(seats, 5, True)
assert get_raw(seats) == test_raw_3

seats = all_rules(seats, 5, True)
print(test_raw_3)
print('\n')
print(get_raw(seats))
print('\n')
print(test_raw_4)

print(count_adjacent(get_seats(test_raw_3), 0, 3, True))
assert get_raw(seats) == test_raw_4

seats = all_rules(seats, 5, True)
print(get_raw(seats))
assert get_raw(seats) == test_raw_5

seats = all_rules(seats, 5, True)
print(get_raw(seats))
assert get_raw(seats) == test_raw_6
# %%
seats = get_seats(test_raw)
seats = find_equilibrium(seats, 5, True)
print(count_occupied(seats))
assert count_occupied(seats) == 26
