from typing import Tuple, List, Dict, DefaultDict
from collections import defaultdict

DIRECTIONS = {'ne': (1, 0), 'e': (0, 1), 'se': (-1, 1), 'sw': (-1, 0), 'w': (0, -1), 'nw': (1, -1)}
Coord = Tuple[int, int]


class Floor:
    def __init__(self, raw: str) -> None:
        # use ne and e as unit vectors
        # ne = (1,0), e = (0,1)
        self.tiles: Dict[Coord, str]
        # only store black tiles, if the tile is white it is not stored in self.tiles.

        self.set_tiles(raw)

    def set_tiles(self, raw: str) -> None:
        def parse(line: str) -> Coord:
            dir_str = ''
            coord_ne, coord_e = 0, 0
            for char in line:
                dir_str += char
                if dir_str in DIRECTIONS.keys():
                    dir_vec = DIRECTIONS[dir_str]
                    coord_ne += dir_vec[0]
                    coord_e += dir_vec[1]
                    dir_str = ''
            return coord_ne, coord_e

        self.tiles = {}
        for line in raw.splitlines():
            coord = parse(line)
            if coord in self.tiles:
                del self.tiles[coord]
            else:
                self.tiles[coord] = 'black'

    def all_adj_coords(self) -> List[Tuple[int, int]]:
        return [(coord[0] + ne, coord[1] + e) for ne, e in DIRECTIONS.values()
                for coord in self.tiles]

    def count_black_adj(self) -> Dict[Coord, int]:
        num_black_adj: DefaultDict[Coord, int] = defaultdict(int)
        for adj_coord in self.all_adj_coords():
            num_black_adj[adj_coord] += 1
        return num_black_adj

    def step(self) -> None:
        # Any black tile with zero or more than 2 black tiles immediately adjacent
        # to it is flipped to white.
        # Any white tile with exactly 2 black tiles immediately adjacent to it
        # is flipped to black.
        new_tiles = {}
        num_black_adj = self.count_black_adj()
        for adj_coord in self.all_adj_coords():
            num_b_adj = num_black_adj[adj_coord]
            if adj_coord not in self.tiles and num_b_adj == 2:
                new_tiles[adj_coord] = 'black'
            elif adj_coord in self.tiles and (num_b_adj > 2 or num_b_adj == 0):
                pass
            elif adj_coord in self.tiles:
                new_tiles[adj_coord] = self.tiles[adj_coord]
        self.tiles = new_tiles

    def step_n_days(self, n: int) -> None:
        for i in range(n):
            self.step()

    def count_black(self) -> int:
        return sum(1 if colour == 'black' else 0 for colour in self.tiles.values())


#
# Unit Tests
#

TEST_RAW = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

floor = Floor(TEST_RAW)
assert floor.count_black() == 10

floor.step_n_days(100)
assert floor.count_black() == 2208

#
# Problem
#

with open('inputs/24.txt') as file:
    RAW = file.read()

floor = Floor(RAW)
print(floor.count_black())

floor.step_n_days(100)
print(floor.count_black())
