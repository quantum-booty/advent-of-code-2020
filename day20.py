from typing import List, Dict, Set, DefaultDict, Tuple, Any
import re
import numpy as np
from collections import defaultdict


class Config:
    def __init__(self, tile: np.ndarray):
        self.sides: Dict[int, str] = self.set_sides(tile)
        # each side will have a set of matching (id, configuration, side)
        self.matches: DefaultDict[int, Set[Tuple[int, int, int]]] = defaultdict(set)
        self.tile: np.ndarray = tile

    @staticmethod
    def set_sides(tile: np.ndarray) -> Dict[int, str]:
        sides = {}
        # up
        sides[0] = ''.join(tile[0])
        # right
        sides[1] = ''.join(tile[:, -1])
        # down
        sides[2] = ''.join(tile[-1])
        # left
        sides[3] = ''.join(tile[:, 0])
        return sides

    def __str__(self) -> str:
        config_str = ''
        for row in self.tile:
            row_str = ''.join(row)
            config_str += row_str + '\n'
        return config_str.strip()


class Tile:
    def __init__(self, tile_raw) -> None:
        self.configs: Dict[int, Config]
        self.tile: np.ndarray

        self.set_tile_sides(tile_raw)

    def set_tile_sides(self, tile_raw: str) -> None:
        self.tile = np.array([list(line) for line in tile_raw.splitlines()])

        new_tile = np.copy(self.tile)
        self.configs = {}

        for config_id in range(0, 4):
            if config_id != 0:
                new_tile = np.rot90(new_tile)
            self.configs[config_id] = Config(new_tile)

            # y reflection
            self.configs[config_id + 4] = Config(new_tile[::-1])

            if False:
                # for diagnostics
                sorted_configs = {}
                for key, value in sorted(self.configs.items()):
                    sorted_configs[key] = value
                self.configs = sorted_configs


class JigsawPuzzle:
    def __init__(self, raw: str) -> None:
        self.tiles: Dict[int, Tile] = self.set_tiles(raw)
        self.set_tile_matches()
        self.corner_tiles: Dict[int, Tile]
        self.non_corner_tiles: Dict[int, Tile]
        self.inner_tiles: Dict[int, Tile]
        self.find_border_tiles()
        self.grid: List[List[Config]]
        self.init_grid()
        self.counterclock_fill()
        self.downward_fill()

    def set_tiles(self, raw: str) -> Dict[int, Tile]:
        tiles_raw = raw.split('\n\n')
        tiles = {}
        for tile_raw in tiles_raw:
            id_raw, tile_raw = tile_raw.split(':')
            id_match = re.search(r'(\d+)', id_raw)
            if id_match:
                id = id_match.group(0)
            else:
                raise ValueError('ID not a number?')

            tiles[int(id)] = Tile(tile_raw.strip())
        return tiles

    def set_tile_matches(self) -> None:
        for tile_id, tile in self.tiles.items():
            for other_tile_id, other_tile in self.tiles.items():
                if tile_id == other_tile_id:
                    continue

                for config_id, config in tile.configs.items():
                    for side_id, side in config.sides.items():
                        for other_config_id, other_config in other_tile.configs.items():
                            for other_side_id, other_side in other_config.sides.items():

                                condition = (side_id == 0
                                             and other_side_id == 2) or (side_id == 1
                                                                         and other_side_id == 3)

                                if (side == other_side) and condition:
                                    other_ids = (other_tile_id, other_config_id, other_side_id)
                                    self.tiles[tile_id].configs[config_id].matches[side_id] |= {
                                        other_ids
                                    }

                                    ids = (tile_id, config_id, side_id)
                                    self.tiles[other_tile_id].configs[other_config_id].matches[
                                        other_side_id] |= {ids}

    def find_border_tiles(self) -> None:
        self.corner_tiles = dict()
        self.non_corner_tiles = dict()
        self.inner_tiles = dict()
        for tile_id, tile in self.tiles.items():
            if all(map(lambda x: len(x) <= 3,
                       [config.matches for config in tile.configs.values()])):
                # The number of matches are the same for any configs in a corner tile!
                assert len(set([len(config.matches) for config in tile.configs.values()])) == 1
                for config_id, config in tile.configs.items():
                    if len(config.matches) == 3:
                        # Not corner
                        self.non_corner_tiles[tile_id] = tile
                    if len(config.matches) == 2:
                        # Corner
                        self.corner_tiles[tile_id] = tile
            else:
                # has 4 matching sides, therefore is an inner tile.
                self.inner_tiles[tile_id] = tile

    def part1(self) -> int:
        # part 1 answer, the product of corner tile ids
        return np.prod(list(self.corner_tiles.keys()))

    @staticmethod
    def from_to(from_row, from_col, from_side_id: int, to_side_id: int) -> Tuple[int, int]:
        if from_side_id == 0 and to_side_id == 2:
            to_row, to_col = from_row - 1, from_col
        elif from_side_id == 2 and to_side_id == 0:
            to_row, to_col = from_row + 1, from_col
        elif from_side_id == 1 and to_side_id == 3:
            to_row, to_col = from_row, from_col + 1
        elif from_side_id == 3 and to_side_id == 1:
            to_row, to_col = from_row, from_col - 1
        else:
            raise ValueError
        return to_row, to_col

    def initialize_config(self) -> Config:
        init_config = None
        for tile_id, corner_tile in self.corner_tiles.items():
            # Choose a corner_tile and one configuration to get started
            # I choose top left coner config with matching side_ids == 1 and 2.
            for config_id, init_config in corner_tile.configs.items():
                if list(init_config.matches.keys()) == [1, 2]:
                    init_config = init_config
                    break
            break
        if init_config:
            return init_config
        else:
            raise ValueError

    def init_grid(self) -> None:
        init_config = self.initialize_config()
        puzzle_side_len = int(len(self.tiles)**0.5)
        row_list = [None] * puzzle_side_len
        grid: List[List[Any]]
        grid = [row_list * 1 for i in range(puzzle_side_len)]
        grid[0][0] = init_config
        self.grid = grid

    def print_grid(self) -> None:
        grid = [[1 if col else 0 for col in row] for row in self.grid]
        print(np.array(grid))

    def counterclock_fill(self, from_row=0, from_col=0) -> None:
        """start from top left corner
        fill rightward until hit wall
        fill downward until hit wall
        fill leftward until hit wall
        fill upward until top left."""

        for to_side_id_goal in [3, 0, 1, 2]:
            for step in range(len(self.grid) - 1):
                for from_side_id, matching_set in self.grid[from_row][from_col].matches.items():
                    assert len(matching_set) == 1
                    to_tile_id, to_config_id, to_side_id = [match for match in matching_set][0]
                    if to_side_id == to_side_id_goal:
                        to_row, to_col = self.from_to(from_row, from_col, from_side_id, to_side_id)
                        self.grid[to_row][to_col] = self.tiles[to_tile_id].configs[to_config_id]
                        from_row, from_col = to_row, to_col

    def downward_fill(self) -> None:
        """The border can uniquely determine the adjacent inner border
        So I will start with top border and fill downward."""
        side_len = len(self.grid)
        for row in range(1, side_len):
            for col in range(1, side_len):
                for from_side_id, matching_set in self.grid[row - 1][col].matches.items():
                    assert len(matching_set) == 1
                    to_tile_id, to_config_id, to_side_id = [match for match in matching_set][0]

                    # downward we go!
                    if to_side_id == 0:
                        self.grid[row][col] = self.tiles[to_tile_id].configs[to_config_id]

    @staticmethod
    def array_to_str(array: np.ndarray) -> str:
        string = ''
        for row in array:
            row_str = ''.join(row)
            string += row_str + '\n'
        return string.strip()

    def grid_to_str(self, trim_sides=False) -> str:
        grid_str = ''
        n_row = len(self.grid[0][0].tile)
        n_col = len(self.grid[0][0].tile[0])
        zero_array = np.full((n_row, n_col), '.')
        for i, row in enumerate(self.grid):
            array = self.grid[i][0].tile
            if trim_sides:
                array = array[1:-1, 1:-1]
            for j, config in enumerate(row):
                if j == 0:
                    continue
                try:
                    arr = config.tile
                    if trim_sides:
                        arr = arr[1:-1, 1:-1]
                    array = np.concatenate([array, arr], axis=1)
                except Exception:
                    arr = zero_array
                    if trim_sides:
                        arr = arr[1:-1, 1:-1]
                    array = np.concatenate([array, arr], axis=1)
            grid_str += self.array_to_str(array) + '\n'

        return grid_str.strip()

    @staticmethod
    def image_matches(image_arr: np.ndarray, monster_arr: np.ndarray, sea_monster) -> int:
        mon_len_row, mon_len_col = monster_arr.shape
        img_len_row, img_len_col = image_arr.shape

        count = 0
        for row in range(img_len_row):
            for col in range(img_len_col):
                if img_len_row - row < mon_len_row or img_len_col - col < mon_len_col:
                    continue
                sub_image = image_arr[row:row + mon_len_row, col:col + mon_len_col]
                sub_image_str = puzzle.array_to_str(sub_image)
                match = re.match(sea_monster.replace('\n', ''), sub_image_str.replace('\n', ''))
                if match:
                    count += 1
        return count

    def part2(self, sea_monster) -> int:

        image = self.grid_to_str(trim_sides=True)
        image_arr = np.array([list(line) for line in image.splitlines()])
        monster_arr = np.array([list(line) for line in sea_monster.splitlines()])
        count = 0
        for i in range(4):
            if i != 0:
                image_arr = np.rot90(image_arr)
            count += self.image_matches(image_arr, monster_arr, sea_monster)

            # y reflection
            image_arr = image_arr[::-1]
            count += self.image_matches(image_arr, monster_arr, sea_monster)

            # x reflection
            image_arr = image_arr[:, ::-1]
            count += self.image_matches(image_arr, monster_arr, sea_monster)

        tot_hash = sum(1 if char == "#" else 0
                       for char in image) - count * sum(1 if char == "#" else 0
                                                        for char in sea_monster)
        print(image)
        return tot_hash


with open('inputs/20.txt') as file:
    RAW = file.read()

puzzle = JigsawPuzzle(RAW)

print(puzzle.part1())

sea_monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.replace(' ', '.')
print(sea_monster)
print(puzzle.part2(sea_monster))
