from typing import NamedTuple, List, Tuple
from numpy import cos, sin, pi
import numpy as np

# position information: direction facing, x and y
# NESW would change x and y, and is independent of L and R
# L, R changes direction
# F means move in the direction plane is facing
# F*(cos(theta), sin(theta))


class Action(NamedTuple):
    action: str
    value: int


Actions = List[Action]


def get_actions(raw: str) -> Actions:
    actions = []
    for line in raw.splitlines():
        action = Action(line[0], int(line[1:]))
        actions.append(action)
    return actions


Coord = Tuple[int, int]


def do_actions(actions: Actions) -> Coord:
    x = 0
    y = 0
    theta = 0
    for a in actions:
        if a.action == 'N':
            y += a.value
        elif a.action == 'S':
            y -= a.value
        elif a.action == 'E':
            x += a.value
        elif a.action == 'W':
            x -= a.value
        elif a.action == 'L':
            theta += a.value
        elif a.action == 'R':
            theta -= a.value
        elif a.action == 'F':
            angle = theta / 180 * pi
            x += a.value * int(cos(angle))
            y += a.value * int(sin(angle))
    return x, y


def manhat_dist(xi, yi, xf, yf):
    return abs(xf - xi) + abs(yf - yi)


def do_actions_2(actions: Actions) -> Coord:
    x = 0    # ship
    y = 0    # ship
    xw = 10    # waypoint
    yw = 1    # waypoint
    for a in actions:
        if a.action == 'N':
            yw += a.value
        elif a.action == 'S':
            yw -= a.value
        elif a.action == 'E':
            xw += a.value
        elif a.action == 'W':
            xw -= a.value

        elif a.action == 'L':
            theta = a.value / 180 * pi
            rot_mat = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
            coord_way = rot_mat @ np.array([xw, yw])
            xw = coord_way[0]
            yw = coord_way[1]
        elif a.action == 'R':
            theta = -a.value / 180 * pi
            rot_mat = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
            coord_way = rot_mat @ np.array([xw, yw])
            xw = coord_way[0]
            yw = coord_way[1]
        elif a.action == 'F':
            x += a.value * xw
            y += a.value * yw
    return int(x), int(y)


#
# Unit tests
#

test_raw = """F10
N3
F7
R90
F11"""

actions = get_actions(test_raw)
x, y = do_actions(actions)
assert manhat_dist(0, 0, x, y) == 25

x, y = do_actions_2(actions)
assert manhat_dist(0, 0, x, y) == 286

#
# Problem
#

# part 1
with open('inputs/12.txt', 'r') as file:
    raw = file.read()

actions = get_actions(raw)
x, y = do_actions(actions)
print(manhat_dist(0, 0, x, y))

# part 2

x, y = do_actions_2(actions)
print(manhat_dist(0, 0, x, y))
