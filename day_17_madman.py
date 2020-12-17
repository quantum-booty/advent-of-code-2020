#
# This is the madman solution, I've made it extensible to arbitrary dimensions.
# Its more complicated than it sould be, because I'm retarded enough to dictionary instead of numpy array.
#
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

from typing import List, Dict, Tuple
import itertools
import copy
from collections import defaultdict


class HyperCube:
    def __init__(self,
                 raw: str,
                 dimensions: List[str] = ['x', 'y', 'z'],
                 goal_dim: int = 3) -> None:
        self.is_active: Dict[int, Dict]
        self.ranges: Dict[str, List[int]]

        self.set_is_active(raw, goal_dim)
        self.set_ranges(dimensions)

    def get_is_active_coord(self, coord: Tuple[int, ...]) -> int:
        value = self.is_active
        for dim in coord[::-1]:
            value = value[dim]
        if not isinstance(value, int):
            raise ValueError
        else:
            return value

    @staticmethod
    def set_is_active_coord(is_active, coord: Tuple[int, ...], value) -> None:
        for dim in coord[::-1]:
            is_active = is_active.setdefault(dim, {})
        is_active[coord[-1]] = value

    def set_is_active(self, raw: str, goal_dim: int) -> None:
        # TODO: This is fucked!
        def nest_defaultdict(goal_dim, nested_dd, current_dim=2):
            print(nested_dd)
            if current_dim == goal_dim:
                return nested_dd
            else:
                nested_dd = defaultdict(lambda: nested_dd)
                return nest_defaultdict(goal_dim, nested_dd, current_dim + 1)

        self.is_active = defaultdict(lambda: defaultdict(lambda: 0))
        for y, line in enumerate(raw.splitlines()):
            for x, char in enumerate(line):
                if char == '#':
                    self.is_active[y][x] = 1
                else:
                    self.is_active[y][x] = 0

        self.is_active = nest_defaultdict(goal_dim, self.is_active)

    def set_ranges(self, dimensions: List[str]) -> None:
        self.ranges = {}

        def get_range(is_active_subdim: Dict, goal_dim: int, current_dim=0) -> List[int]:
            if current_dim == goal_dim:
                return list(is_active_subdim.keys())
            else:
                return get_range(is_active_subdim[0], goal_dim, current_dim + 1)

        for goal_dim, dim in enumerate(dimensions):
            self.ranges[dim] = get_range(self.is_active, goal_dim)

    def count_active_neighbours(self, coord: Tuple[int, ...]) -> int:
        ranges = [range(c - 1, c + 2) for c in coord]
        neighbours = itertools.product(*ranges)
        a_neighbours = 0
        for curr_coord in neighbours:
            if curr_coord == coord:
                continue
            neighbour = self.is_active
            for dim in curr_coord[::-1]:
                neighbour = neighbour[dim]

            if isinstance(neighbour, int):
                a_neighbours += neighbour
            else:
                raise ValueError
        return a_neighbours

    def expand_ranges(self) -> None:
        def expand_range(range):
            return [min(range) - 1] + range + [max(range) + 1]

        for dim in self.ranges:
            self.ranges[dim] = expand_range(self.ranges[dim])

    def step(self) -> None:
        is_active_new = copy.deepcopy(self.is_active)
        self.expand_ranges()

        for coord in itertools.product(*self.ranges.values()):
            a_neighbours = self.count_active_neighbours(coord)
            is_active = self.get_is_active_coord(coord)
            if is_active and a_neighbours in (2, 3):
                continue
            elif not is_active and a_neighbours == 3:
                self.set_is_active_coord(is_active_new, coord, 1)
            else:
                # This makes sure that the dimensions are the same within zdim, ydim, xdim
                self.set_is_active_coord(is_active_new, coord, 0)

        self.is_active = is_active_new

    def get_tot_active(self):
        tot_active = 0
        for coord in itertools.product(*self.ranges.values()):
            tot_active += self.get_is_active_coord(coord)
        return tot_active

    def get_tot_active_at_cycle(self, cycles: int = 6) -> int:
        for cycle in range(cycles):
            self.step()
        return self.get_tot_active()


#
# Unit tests
#

cube = HyperCube(TEST_RAW)
cube.is_active
# cube.ranges

# %%

assert cube.get_tot_active_at_cycle() == 112

#
# Problem
#

cube = HyperCube(RAW)
print(cube.get_tot_active_at_cycle())
