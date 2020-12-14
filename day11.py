from typing import List, Tuple
from copy import deepcopy

Seats = List[List[str]]


def get_seats(raw: str) -> Seats:
    seats = [list(line) for line in raw.splitlines()]
    return seats


def get_raw(seats: Seats) -> str:
    raw = '\n'.join(''.join(line) for line in seats)
    return raw


def get_dims(seats) -> Tuple[int, int]:
    width = len(seats[0])
    height = len(seats)
    return width, height


def count_adjacent(seats: Seats, i: int, j: int, visible) -> int:
    width, height = get_dims(seats)
    count = 0
    directions = [[1, 0], [-1, 0], [1, 1], [-1, -1], [0, 1], [0, -1], [-1, 1], [1, -1]]
    for dir in directions:
        pos = [i, j]
        while True:
            pos = [pos[0] + dir[0], pos[1] + dir[1]]
            if pos[0] == -1 or pos[0] == height or pos[1] == -1 or pos[1] == width:
                # Don't sit outside the airplane!
                break

            if visible:
                if seats[pos[0]][pos[1]] == 'L':
                    # Empty seat blocks visibility
                    break

            if seats[pos[0]][pos[1]] == '#':
                count += 1
                break

            if not visible:
                # Only search for adjacent seats
                break

    return count


def all_rules(seats: Seats, tolerance=4, visible=False) -> Seats:
    old_seats = seats
    new_seats = deepcopy(seats)
    width, height = get_dims(seats)
    for i in range(height):
        for j in range(width):
            num_adj = count_adjacent(old_seats, i, j, visible)
            if old_seats[i][j] == 'L' and num_adj == 0:
                new_seats[i][j] = '#'
            elif old_seats[i][j] == '#' and num_adj >= tolerance:
                new_seats[i][j] = 'L'
    return new_seats


def find_equilibrium(seats: Seats, tolerance=4, visible=False) -> Seats:
    old_seats = seats
    new_seats = None
    count = 0
    while True:
        count += 1
        new_seats = all_rules(old_seats, tolerance, visible)
        if old_seats == new_seats:
            return new_seats
        old_seats = new_seats


def count_occupied(seats: Seats) -> int:
    return sum(sum(1 if seat == '#' else 0 for seat in line) for line in seats)


if __name__ == "__main__":
    with open('inputs/11.txt', 'r') as file:
        raw = file.read()

    # part 1
    seats = get_seats(raw)
    seats = find_equilibrium(seats)
    print(count_occupied(seats))

    # part 2
    seats = get_seats(raw)
    seats = find_equilibrium(seats, 5, True)
    print(count_occupied(seats))
