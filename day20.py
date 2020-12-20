from typing import List, Dict, Set, DefaultDict, Tuple
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

            # x reflection
            self.configs[config_id + 8] = Config(new_tile[:, ::-1])

            sorted_configs = {}
            for key, value in sorted(self.configs.items()):
                sorted_configs[key] = value
            self.configs = sorted_configs


class JigsawPuzzle:
    def __init__(self, raw: str) -> None:
        self.tiles: Dict[int, Tile] = self.set_tiles(raw)
        self.set_tile_matches()

    def set_tiles(self, raw: str) -> Dict[int, Tile]:
        tiles_raw = raw.replace('#', '1').replace('.', '0').split('\n\n')
        tiles = {}
        for tile_raw in tiles_raw:
            id_raw, tile_raw = tile_raw.split(':')
            id_match = re.search(r'(\d+)', id_raw)
            if id_match:
                id = id_match.group(0)
            else:
                raise ValueError('ID not not a number?')

            tiles[int(id)] = Tile(tile_raw.strip())
        return tiles

    def set_tile_matches(self) -> None:
        for tile_id, tile in self.tiles.items():
            for config_id, config in tile.configs.items():
                for side_id, side in config.sides.items():

                    for other_tile_id, other_tile in self.tiles.items():
                        if tile_id == other_tile_id:
                            continue

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


with open('inputs/20_part1_test.txt') as file:
    TEST_RAW_1 = file.read()

with open('inputs/20.txt') as file:
    RAW = file.read()

# puzzle = JigsawPuzzle(TEST_RAW_1)
puzzle = JigsawPuzzle(RAW)

border_tiles = dict()
corner_tiles = dict()
non_corner_tiles = dict()
for tile_id, tile in puzzle.tiles.items():
    if all(map(lambda x: len(x) <= 3, [config.matches for config in tile.configs.values()])):
        border_tiles[tile_id] = tile
        # print(tile_id)
        # The number of matches are the same for any configs in a corner tile!
        assert len(set([len(config.matches) for config in tile.configs.values()])) == 1
        for config_id, config in tile.configs.items():
            if len(config.matches) == 3:
                # Not corner
                non_corner_tiles[tile_id] = tile
            if len(config.matches) == 2:
                # Corner
                corner_tiles[tile_id] = tile
print(np.prod(list(corner_tiles.keys())))
