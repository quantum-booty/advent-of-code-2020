# This is a more memory effecient way, rather than creating a grid, I am only
# keeping track of the active cubes.
# This also a very good example of "explicit is better than implicit!" Because
# I used defaultdict, I have to mentally keep track of all the default values,
# and this has caused some trouble debugging!

from typing import Tuple, DefaultDict
from collections import defaultdict
import itertools
"""
* . is inactive, # is active
* a game can see its 26 immidiate neighbours
* if a game is active and exactly 2 or 3 of its neighbours are active, it remains
active. Otherwise it becomes inactive.
* If a game is inactive but exactly 3 of its neighbours are active, the game
becomes active. Otherwise it remains inactive.
* How many cubes are active after the sixth cycle?
"""

# use defaultdict instead of namedtuple for Point because it needs to be mutable.
Index = Tuple[int, ...]
Point = DefaultDict[str, int]
Points = DefaultDict[Index, Point]


class GameofLife:
    def __init__(self, raw: str, n_dims=3) -> None:
        self.points: Points
        self.set_points(raw, n_dims)
        self.cycle: int = 0

    def set_points(self, raw: str, goal_dim: int) -> None:
        self.points = defaultdict(lambda: defaultdict(int))
        for y, line in enumerate(raw.splitlines()):
            for x, char in enumerate(line):
                index = (x, y) + (0, ) * (goal_dim - 2)
                if char == '#':
                    self.points[index]['is_active'] = 1

    def set_candidates(self) -> None:
        # Each active point will reproduce new points at its neighbours, and
        # increase its population (the number of neighbours the new point can see).
        new_points: Points = defaultdict(lambda: defaultdict(int))
        for index in self.points:
            # the existing points are all active
            new_points[index]['is_active'] = 1
            neighbour_indices = itertools.product(*[range(i - 1, i + 2) for i in index])
            for neighbour_index in neighbour_indices:
                if neighbour_index == index:
                    # don't change the population of the point it self!
                    continue
                new_points[neighbour_index]['population'] += 1
        self.points = new_points

    def step(self) -> None:
        self.set_candidates()
        new_points: Points = defaultdict(lambda: defaultdict(int))
        for index in self.points:
            a_neighbours = self.points[index]['population']
            is_active = self.points[index]['is_active']
            if is_active and a_neighbours in (2, 3):
                new_points[index]['is_active'] = 1
            elif not is_active and a_neighbours == 3:
                new_points[index]['is_active'] = 1
        self.points = new_points
        # dict comprehension method, slightly faster than the for loop
        # although it looks nicer it produce Dict type rather than defaultdict.
        # I'm not a bit fan of types mixing.

        # self.points = {
        #     index: point
        #     for index, point in self.points.items()
        #     if point['is_active'] == 1 and point['population'] in (2, 3)
        #     or point['is_active'] == 0 and point['population'] == 3
        # }

    def get_tot_active_at_cycle(self, cycle_goal: int = 6) -> int:
        assert cycle_goal > self.cycle
        while self.cycle != cycle_goal:
            self.step()
            self.cycle += 1
        return len(self.points)


TEST_RAW = """.#.
..#
###"""

#
# Unit tests
#
game = GameofLife(TEST_RAW, n_dims=3)
assert game.get_tot_active_at_cycle() == 112

game = GameofLife(TEST_RAW, n_dims=4)
assert game.get_tot_active_at_cycle() == 848

#
# Problem
#

RAW = """##.#....
...#...#
.#.#.##.
..#.#...
.###....
.##.#...
#.##..##
#.####.."""

game = GameofLife(RAW, n_dims=3)
print(game.get_tot_active_at_cycle())

game = GameofLife(RAW, n_dims=4)
print(game.get_tot_active_at_cycle())
