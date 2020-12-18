from typing import Tuple
import itertools
import numpy as np
import copy
"""
* . is inactive, # is active
* a cube can see its 26 immidiate neighbours
* if a cube is active and exactly 2 or 3 of its neighbours are active, it remains
active. Otherwise it becomes inactive.
* If a cube is inactive but exactly 3 of its neighbours are active, the cube
becomes active. Otherwise it remains inactive.
* How many cubes are active after the sixth cycle?
"""


class HyperCube:
    def __init__(self, raw: str, n_dims=3) -> None:
        self.grid: np.ndarray
        self.set_grid(raw, n_dims)
        self.cycle: int = 0

    def set_grid(self, raw: str, goal_dim: int) -> None:
        y_list = []
        for y, line in enumerate(raw.splitlines()):
            x_list = []
            for x, char in enumerate(line):
                if char == '#':
                    x_list.append(1)
                else:
                    x_list.append(0)
            y_list.append(x_list)

        self.grid = y_list
        for d in np.arange(0, goal_dim - 2):
            self.grid = [self.grid]
        self.grid = np.array(self.grid)

    def count_active_neighbours(self, index: Tuple[int, ...]) -> int:
        neighbour_slicer = [slice(i - 1, i + 2) if i != 0 else slice(0, 2) for i in index]
        neighbours = self.grid[tuple(neighbour_slicer)]
        a_neighbours = neighbours.sum() - self.grid[index]
        return a_neighbours

    def pad_grid(self) -> None:
        new_grid = np.zeros([d + 2 for d in self.grid.shape])
        new_grid[tuple(slice(1, -1) for d in self.grid.shape)] = self.grid
        self.grid = new_grid

    def step(self) -> None:
        self.pad_grid()
        new_grid = np.copy(self.grid)

        for index in itertools.product(*[range(d) for d in self.grid.shape]):
            a_neighbours = self.count_active_neighbours(index)
            is_active = self.grid[index]
            if is_active and a_neighbours in (2, 3):
                continue
            elif not is_active and a_neighbours == 3:
                new_grid[index] = 1
            else:
                new_grid[index] = 0

        self.grid = new_grid

    def get_tot_active(self):
        return self.grid.sum()

    def get_tot_active_at_cycle(self, cycle_goal: int = 6) -> int:
        assert cycle_goal > self.cycle
        while self.cycle != cycle_goal:
            self.step()
            self.cycle += 1
        return self.get_tot_active()


TEST_RAW = """.#.
..#
###"""

#
# Unit tests
#
cube = HyperCube(TEST_RAW, n_dims=3)
assert cube.get_tot_active_at_cycle() == 112

cube = HyperCube(TEST_RAW, n_dims=4)
assert cube.get_tot_active_at_cycle() == 848

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

cube = HyperCube(RAW, n_dims=3)
print(cube.get_tot_active_at_cycle())

cube = HyperCube(RAW, n_dims=4)
print(cube.get_tot_active_at_cycle())
