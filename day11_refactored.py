from typing import List, Tuple

Seats = Tuple


def get_seats(raw: str) -> Seats:
    return tuple(raw.replace('\n', ''))


def get_raw(seats, height, width) -> str:
    lines = [''.join(seats[i * width:(i + 1) * width]) for i in range(height)]
    raw = '\n'.join(lines)
    return raw


def get_dims(raw) -> Tuple[int, int]:
    seats = raw.splitlines()
    width = len(seats[0])
    height = len(seats)
    return width, height


directions = ((1, 0), (-1, 0), (1, 1), (-1, -1), (0, 1), (0, -1), (-1, 1), (1, -1))


def count_adjacent(seats: Seats, i: int, j: int, visible, height, width, tolerance) -> int:
    count = 0
    for dir in directions:
        steps = 1
        while True:
            y = i + dir[0] * steps
            x = j + dir[1] * steps
            steps += 1
            if not 0 <= y < height or not 0 <= x < width:
                # Don't sit outside the airplane!
                break

            pos = y * width + x
            seat = seats[pos]
            if visible and seat == 'L':
                # Empty seat blocks visibility
                break

            if seat == '#':
                count += 1
                if count >= tolerance:
                    return count
                break

            if not visible:
                # Only search for adjacent seats
                break

    return count


def all_rules(seats: Seats, tolerance, visible, height, width) -> Tuple[Seats, bool]:
    old_seats = seats
    new_seats = ['.'] * len(seats)
    changed = False
    for i in range(height):
        for j in range(width):
            pos = i * width + j
            if old_seats[pos] == '.':
                continue
            num_adj = count_adjacent(old_seats, i, j, visible, height, width, tolerance)
            # print(num_adj)

            if old_seats[pos] == 'L' and num_adj == 0:
                new_seats[pos] = '#'
                changed = True
            elif old_seats[pos] == '#' and num_adj >= tolerance:
                new_seats[pos] = 'L'
                changed = True
            else:
                new_seats[pos] = old_seats[pos]

    return tuple(new_seats), changed


def find_equilibrium(seats: Seats, tolerance, visible, height, width) -> Seats:
    old_seats = seats
    new_seats = None
    count = 0
    while True:
        count += 1
        new_seats, changed = all_rules(old_seats, tolerance, visible, height, width)
        # if not changed:
        #     return new_seats
        # if not new_seats != old_seats:
        #     return new_seats
        # if new_seats == old_seats:
        #     return new_seats

        old_seats = new_seats


def count_occupied(seats: Seats) -> int:
    return sum(1 if seat == '#' else 0 for seat in seats)


if __name__ == "__main__":
    with open('inputs/11.txt', 'r') as file:
        raw = file.read()

    width, height = get_dims(raw)

    # part 1
    seats = get_seats(raw)
    seats = find_equilibrium(seats, 4, False, height, width)
    print(count_occupied(seats))

    # part 2

    seats = get_seats(raw)
    seats = find_equilibrium(seats, 5, True, height, width)
    print(count_occupied(seats))
