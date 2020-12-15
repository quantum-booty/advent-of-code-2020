# Refactored using ideas from Joel Grus
from typing import NamedTuple, List
from numpy import cos, sin, pi
import numpy as np
from dataclasses import dataclass

# position information: direction facing, x and y
# NESW would change x and y, and is independent of L and R
# L, R changes direction
# F means move in the direction plane is facing
# F*(cos(theta), sin(theta))


class Action(NamedTuple):
    action: str
    value: int

    @staticmethod
    def parse(raw: str):
        return Action(raw[0], int(raw[1:]))


Actions = List[Action]


def get_actions(raw: str) -> Actions:
    return [Action.parse(line) for line in raw.splitlines()]


# Use dataclass because we want the attributes to be mutable
@dataclass
class Ship:
    x: int = 0
    y: int = 0
    theta: int = 0

    def move(self, action: Action) -> None:
        if action.action == 'N':
            self.y += action.value
        elif action.action == 'S':
            self.y -= action.value
        elif action.action == 'E':
            self.x += action.value
        elif action.action == 'W':
            self.x -= action.value
        elif action.action == 'L':
            self.theta += action.value
        elif action.action == 'R':
            self.theta -= action.value
        elif action.action == 'F':
            angle = self.theta / 180 * pi
            self.x += action.value * int(cos(angle))
            self.y += action.value * int(sin(angle))
        else:
            raise ValueError(f'unknown action {action}')

    def do_actions(self, actions: Actions) -> None:
        for a in actions:
            self.move(a)

    def manhat_dist(self) -> int:
        return abs(self.x) + abs(self.y)


@dataclass
class ShipAndWaypoint:
    x: int = 0    # ship
    y: int = 0    # ship
    xw: int = 10    # waypoint
    yw: int = 1    # waypoint

    def rotate_waypoint(self, theta) -> None:
        rot_mat = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
        coord_way = rot_mat @ np.array([self.xw, self.yw])
        self.xw = int(coord_way[0])
        self.yw = int(coord_way[1])

    def move(self, a: Action) -> None:
        if a.action == 'N':
            self.yw += a.value
        elif a.action == 'S':
            self.yw -= a.value
        elif a.action == 'E':
            self.xw += a.value
        elif a.action == 'W':
            self.xw -= a.value

        elif a.action == 'L':
            theta = a.value / 180 * pi
            self.rotate_waypoint(theta)
        elif a.action == 'R':
            theta = -a.value / 180 * pi
            self.rotate_waypoint(theta)
        elif a.action == 'F':
            self.x += a.value * self.xw
            self.y += a.value * self.yw

    def do_actions(self, actions: Actions) -> None:
        for a in actions:
            self.move(a)

    def manhat_dist(self) -> int:
        return abs(self.x) + abs(self.y)


#
# Unit tests
#

test_raw = """F10
N3
F7
R90
F11"""

actions = get_actions(test_raw)
ship = Ship()
ship.do_actions(actions)
assert ship.manhat_dist() == 25

SAW = ShipAndWaypoint()
SAW.do_actions(actions)
assert SAW.manhat_dist() == 286

#
# Problem
#

# part 1
with open('inputs/12.txt', 'r') as file:
    raw = file.read()

actions = get_actions(raw)
ship = Ship()
ship.do_actions(actions)
print(ship.manhat_dist())

# part 2

SAW = ShipAndWaypoint()
SAW.do_actions(actions)
print(SAW.manhat_dist())

SAW2 = ShipAndWaypoint()
SAW2.do_actions(actions)
