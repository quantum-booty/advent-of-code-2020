# legendary code from https://github.com/sophiebits/adventofcode/blob/main/2020/day07.py

from collections import defaultdict
import re

# lines = [line.rstrip('\n') for line in sys.stdin]
with open('inputs/7.txt', 'r') as file:
    input = file.read()

containedin = defaultdict(set)
contains = defaultdict(list)

for line in input.splitlines():
    color = re.match(r'(.+?) bags contain', line)[1]
    for ct, innercolor in re.findall(r'(\d+) (.+?) bags?[,.]', line):
        ct = int(ct)
        containedin[innercolor].add(color)
        contains[color].append((ct, innercolor))

holdsgold = set()


def check(color):
    for c in containedin[color]:
        holdsgold.add(c)
        check(c)


check('shiny gold')
print(len(holdsgold))


def cost(color):
    total = 0
    for ct, inner in contains[color]:
        total += ct
        total += ct * cost(inner)

    return total


print(cost('shiny gold'))
