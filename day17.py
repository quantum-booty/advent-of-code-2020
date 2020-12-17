"""
* . is inactive, # is active
* a cube can see its 26 immidiate neighbours
* if a cube is active and exactly 2 or 3 of its neighbours are active, it remains
active. Otherwise it becomes inactive.
* If a cube is inactive but exactly 3 of its neighbours are active, the cube
becomes active. Otherwise it remains inactive.
* How many cubes are active after the sixth cycle?
"""

RAW = """##.#....
...#...#
.#.#.##.
..#.#...
.###....
.##.#...
#.##..##
#.####.."""

TEST_RAW = """.#.
..#
###"""

from typing import List, Dict, Union, DefaultDict
import itertools
import copy
from collections import defaultdict


class Cube:
    def __init__(self,
                 raw: str,
                 dimensions: List[str] = ['x', 'y', 'z'],
                 goal_dim: int = 3) -> None:
        self.is_active: Dict[int, Dict]
        # self.x_range: List[int]
        # self.y_range: List[int]
        # self.z_range: List[int]
        self.ranges: Dict[str, List[int]]

        self.set_is_active(raw, goal_dim)
        self.set_ranges(dimensions)

    def set_is_active(self, raw: str, goal_dim: int) -> None:
        def nest_defaultdict(goal_dim, nested_dd, current_dim=2):
            if current_dim == goal_dim:
                return nested_dd
            else:
                nested_dd = defaultdict(lambda: nested_dd)
                return nest_defaultdict(nested_dd, goal_dim, current_dim + 1)

        self.is_active = defaultdict(lambda: defaultdict(lambda: 0))
        for y, line in enumerate(raw.splitlines()):
            for x, char in enumerate(line):
                if char == '#':
                    self.is_active[y][x] = 1
                else:
                    self.is_active[y][x] = 0

        self.is_active = nest_defaultdict(goal_dim, self.is_active)

    def set_ranges(self, dimensions) -> None:
        # self.z_range = list(self.is_active.keys())
        # self.y_range = list(self.is_active[0].keys())
        # self.x_range = list(self.is_active[0][0].keys())
        self.ranges = defaultdict(list)

        def get_range(is_active_subdim: Dict, goal_dim: int, current_dim=0) -> List[int]:
            if current_dim == goal_dim:
                return list(is_active_subdim.keys())
            else:
                return get_range(is_active_subdim[0], goal_dim, current_dim + 1)

        for dim in dimensions:
            self.ranges[dim] = get_range(self.is_active, dim)

    def count_active_neighbours(self, x: int, y: int, z: int) -> int:
        # neighbours = [(i, j, k) for i in range(x - 1, x + 2) for j in range(y - 1, y + 2)
        #               for k in range(z - 1, z + 2) if (i, j, k) != (x, y, z)]
        neighbours = itertools.product(range(x - 1, x + 2), range(y - 1, y + 2),
                                       range(z - 1, z + 2))
        a_neighbours = 0
        for i, j, k in neighbours:
            if (i, j, k) == (x, y, z):
                continue
            a_neighbours += self.is_active[k][j][i]
        return a_neighbours

    # def count_active_neighbours(self, x: int, y: int, z: int) -> int:
    #     # neighbours = [(i, j, k) for i in range(x - 1, x + 2) for j in range(y - 1, y + 2)
    #     #               for k in range(z - 1, z + 2) if (i, j, k) != (x, y, z)]
    #     neighbours = itertools.product(range(x - 1, x + 2), range(y - 1, y + 2),
    #                                    range(z - 1, z + 2))
    #     a_neighbours = 0
    #     for i, j, k in neighbours:
    #         if (i, j, k) == (x, y, z):
    #             continue
    #         a_neighbours += self.is_active[k][j][i]
    #     return a_neighbours

    def expand_ranges(self) -> None:
        def expand_range(range):
            return [min(range) - 1] + range + [max(range) + 1]

        for dim in self.ranges:
            self.ranges[dim] = expand_range(self.ranges[dim])

        # self.z_range = expand_range(self.z_range)
        # self.y_range = expand_range(self.y_range)
        # self.x_range = expand_range(self.x_range)

    def step(self) -> None:
        is_active_new = copy.deepcopy(self.is_active)
        self.expand_ranges()

        for x, y, z in itertools.product(self.ranges):

            a_neighbours = self.count_active_neighbours(x, y, z)
            is_active = self.is_active[z][y][x]
            if is_active and a_neighbours in (2, 3):
                continue
            elif not is_active and a_neighbours == 3:
                is_active_new[z][y][x] = 1
            else:
                # This makes sure that the dimensions are the same within zdim, ydim, xdim
                is_active_new[z][y][x] = 0

        self.is_active = is_active_new
        # self.print()

    def get_tot_active(self):
        tot_active = 0
        for x in self.x_range:
            for y in self.y_range:
                for z in self.z_range:
                    tot_active += self.is_active[z][y][x]

        return tot_active

    def part1(self, cycles: int = 6) -> int:
        for cycle in range(cycles):
            self.step()
        return self.get_tot_active()


#
# Unit tests
#

cube = Cube(TEST_RAW)
assert cube.part1() == 112

#
# Problem
#

cube = Cube(RAW)
print(cube.part1())
