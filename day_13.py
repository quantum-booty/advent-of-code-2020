from typing import List, Tuple, Union

IDS = List[Union[int, str]]


def get_time_bus_id(raw: str) -> Tuple[int, IDS]:
    # Earliest departure time, and bus ids
    earl_time, ids = raw.splitlines()
    return int(earl_time), [int(id) if id != 'x' else id for id in ids.split(',')]


def get_earliest_bus(earl_time, ids):
    time = earl_time
    while True:
        time += 1
        for id in ids:
            if id == 'x':
                continue
            elif time % id == 0:
                return id, time


def part1(raw):
    earl_time, ids = get_time_bus_id(raw)
    id, time = get_earliest_bus(earl_time, ids)
    return (time - earl_time) * id


def part2(raw):
    # Brute forced, will never work ( T X T )
    _, ids = get_time_bus_id(raw)
    bus_0_id = ids[0]
    time = ids[0]
    offsets = [i + 1 for i, id in enumerate(ids[1:]) if id != 'x']
    ids = [id for id in ids[1:] if id != 'x']
    while True:
        condition = True
        for offset, id in zip(offsets, ids):
            condition &= (time + offset) % id == 0
            if condition is False:
                time += bus_0_id
                break
        if condition is True:
            return time


test_raw = """939
7,13,x,x,59,x,31,19"""

assert part1(test_raw) == 295

assert part2(test_raw) == 1068781

test_raw_2 = """1
17,x,13,19"""
assert part2(test_raw_2) == 3417
test_raw_2 = """2
67,7,59,61"""
assert part2(test_raw_2) == 754018
test_raw_2 = """1
67,x,7,59,61"""
assert part2(test_raw_2) == 779210
test_raw_2 = """1
67,7,x,59,61"""
assert part2(test_raw_2) == 1261476
test_raw_2 = """1
1789,37,47,1889"""
assert part2(test_raw_2) == 1202161486

with open('inputs/13.txt', 'r') as file:
    raw = file.read()
print(part1(raw))

# print(part2(raw))
