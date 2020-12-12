from typing import List
from collections import Counter

Adapters = List[int]


def get_adapters(raw: str) -> Adapters:
    adapters = [int(num) for num in raw.splitlines()]
    adapters.append(0)
    adapters.append(max(adapters) + 3)
    adapters.sort()
    return adapters


def find_diffs(adapters: Adapters) -> Counter:
    # sort list, iterate from smallist, find the next smallest, find the
    # difference, add difference to dafault dict, find number of 1 diff times 3 diff
    diffs = [adapters[i] - adapters[i - 1] for i in range(1, len(adapters))]
    assert all(1 <= diff <= 3 for diff in diffs)
    return Counter(diffs)


class Node:
    def __init__(self, num, children=[]):
        self.num = num
        self.children = children

    def __str__(self):
        return f'{self.num}'

    def children_num(self):
        return [child.num for child in self.children]


class Graph:
    def __init__(self, nodes: List[Node] = []):
        self.nodes = nodes

    def build_graph(self, adapters: Adapters) -> List[Node]:
        self.nodes = [Node(num) for num in adapters]
        for i in range(len(adapters) - 1):
            if i + 4 < len(adapters):
                n = 4
            else:
                n = len(adapters) - i

            self.nodes[i].children = [
                self.nodes[i + j] for j in range(1, n) if adapters[i] + 3 >= adapters[i + j]
            ]
        return self.nodes

    def traverse(self, start_node: Node = None, traverse_count: int = 0) -> int:
        if start_node is None:
            start_node = self.nodes[0]
        if start_node.num == self.nodes[-1].num:
            return traverse_count + 1
        for child in start_node.children:
            traverse_count = self.traverse(child, traverse_count)
        return traverse_count


#
# Unit tests
#

TEST_RAW1 = """16
10
15
5
1
11
7
19
6
12
4"""

TEST_RAW2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

diffs = find_diffs(get_adapters(TEST_RAW1))
assert diffs[1] == 7 and diffs[3] == 5

diffs = find_diffs(get_adapters(TEST_RAW2))
assert diffs[1] == 22 and diffs[3] == 10

graph = Graph()
graph.build_graph(get_adapters(TEST_RAW1))
assert graph.traverse() == 8

graph = Graph()
graph.build_graph(get_adapters(TEST_RAW2))
assert graph.traverse() == 19208

#
# Problem
#

with open('inputs/10.txt', 'r') as file:
    RAW = file.read()
    adapters = get_adapters(RAW)

# part 1
diffs = find_diffs(adapters)
print(diffs[1] * diffs[3])

# part 2: My recursion method will never terminate.
if False:
    graph = Graph()
    graph.build_graph(adapters)
    for node in graph.nodes:
        print(node, node.children_num())
    graph.traverse()


# The following solutions is from the legend Joel Grus :)
# This is a good example of dynamic progamming!
def count_paths(adapters: Adapters) -> int:
    output = adapters[-1]

    # num_ways[i] is the numbers of ways to get to i
    num_ways = [0] * (output + 1)

    num_ways[0] = 1

    if 1 in adapters:
        num_ways[1] = 1

    if 2 in adapters and 1 in adapters:
        num_ways[2] = 2
    elif 2 in adapters:
        num_ways[2] = 1

    for n in range(3, output + 1):
        if n not in adapters:
            continue

        # One can only get to a number from n-3, n-2 and n-1, there for the
        # numbers of ways to get to n is the sum of the number of ways to get
        # to previous three.
        num_ways[n] = num_ways[n - 3] + num_ways[n - 2] + num_ways[n - 1]

    return num_ways[output]


print(count_paths(adapters))
