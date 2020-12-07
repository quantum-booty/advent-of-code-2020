from typing import List
import os
print(os.getcwd())
os.chdir(
    '/home/henryw/Documents/Study/Computer_Programming_for_Data_Scientists/advent-of-code-2020/')
""" Solution:
 This is a tree problem. Each bag can contain other types of bags.
 Build tree:
     find unique lines
     iterate these lines
     build list of nodes:
        Each bag can be moduled as a tree node with cargo = bag type and number
        bags. The numbers in input is followed by 2 word that describe that bag
        type. Can use re module to find the position of the numbers and then
        find the bag type.
     for each nodes iterate the list of nodes:
         if node's child matches with node that is not it self:
             link node to childs
         else: do nothing
Once we have the tree:
    for each node, recursively search childs until find the wanted child (shiny gold)
    if found, add to total found number

Part 2:
    recursively add this shit
"""


class Node:
    def __init__(self, name: str, nums: List[int] = [], child_names: List[str] = [], children=[]):
        self.name = name
        self.nums = nums
        self.child_names = child_names
        self.children = children

    def __str__(self):
        values = f"""
{self.name}
{self.nums}
{self.child_names}
------------------------------------------------------"""
        return values

    def search(self, desired_name):
        def _search(node, desired_name):
            if node is not None:
                if node.name == desired_name:
                    return True
                else:
                    result = [_search(child, desired_name) for child in node.children]
                return any(result)

        result = [_search(child, desired_name) for child in self.children]
        if any(result):
            return True
        else:
            return False

    def tot_num(self):
        def _tot_num(node):

            tot = 0
            for i, num in enumerate(node.nums):
                tot += num * _tot_num(node.children[i])
            tot += sum(node.nums)

            return tot

        tot = sum(num * _tot_num(node)
                  for num, node in zip(self.nums, self.children)) + sum(self.nums)
        return tot


def get_int_pos(words: List[str]) -> List[int]:
    i = 0
    pos = []
    for word in words:
        try:
            int(word)
            pos.append(i)
        except ValueError:
            pass
        i += 1
    return pos


def build_connections(all_bags: List[Node]) -> List[Node]:
    for bag1 in all_bags:
        children = []
        for bag2 in all_bags:
            if bag2.name in bag1.child_names:
                children.append(bag2)
        bag1.children = children
    return all_bags


def make_bags(raw: str) -> List[Node]:
    all_bags = []
    for line in list(set(raw.splitlines())):
        words = line.split(' ')
        pos = get_int_pos(words)
        bag_numbers = [int(words[i]) for i in pos]
        bag_names = ['_'.join(words[i + 1:i + 3]) for i in pos]

        bag = Node(name='_'.join(words[:2]), nums=bag_numbers, child_names=bag_names)
        all_bags.append(bag)

    all_bags = build_connections(all_bags)
    return all_bags


# test part 1
test_raw = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

all_bags = make_bags(test_raw)
tot = sum([bag.search('shiny_gold') for bag in all_bags])
assert tot == 4

print([bag.search('shiny_gold') for bag in all_bags])

# %% part 1

with open('inputs/7.txt') as file:
    raw = file.read()
all_bags = make_bags(raw)
tot = sum([bag.search('shiny_gold') for bag in all_bags])
print(tot)

# %% test part 2 1
test_raw = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

test_raw = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain 5 dotted black bags.
dotted black bags contain no other bags."""

all_bags = make_bags(test_raw)
shiny_gold = [bag for bag in all_bags if bag.name == 'shiny_gold'][0]
shiny_gold.tot_num()

# %% test part 2 2

test_raw = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

all_bags = make_bags(test_raw)
shiny_gold = [bag for bag in all_bags if bag.name == 'shiny_gold'][0]
shiny_gold.tot_num()

# %% part 2

all_bags = make_bags(raw)
shiny_gold = [bag for bag in all_bags if bag.name == 'shiny_gold'][0]
shiny_gold.tot_num()
