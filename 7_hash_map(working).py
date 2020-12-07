from typing import Dict, List, Tuple

bags: Dict[str, Dict[str, int]]


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


def make_bag(line: str) -> Tuple[str, Dict]:
    words = line.split(' ')
    pos = get_int_pos(words)
    contain_numbers = [int(words[i]) for i in pos]
    contain_types = ['_'.join(words[i + 1:i + 3]) for i in pos]
    bag = {bag_type: number for bag_type, number in zip(contain_types, contain_numbers)}
    bag_type = '_'.join(words[:2])
    return bag_type, bag


def make_bags(raw: str) -> Dict[str, Dict[str, int]]:
    bags = {}
    for line in list(set(raw.splitlines())):
        bag_type, bag = make_bag(line)
        bags[bag_type] = bag
    return bags


def search_bag(bags, starting_bag: Dict, desired_bag='shiny_gold'):
    """for any starting_bag find its childs, check if desired_bag is in its
    childs recursively. """
    if desired_bag in starting_bag.keys():
        return True
    else:
        result = [search_bag(bags, bags[bag_type]) for bag_type in starting_bag]
    return any(result)


def tot_eventual_bags(bags, desired_bag='shiny_gold'):
    return sum(search_bag(bags, bag, desired_bag) for type, bag in bags.items())


def tot_contained_bags(bags, starting_bag: Dict):
    """for any starting_bag add tot number of childs plus the number of sub-childs
    the childs contain contain recursively."""
    return sum(starting_bag[type] * tot_contained_bags(bags, bags[type]) + starting_bag[type]
               for type in starting_bag)


# part 1

with open('inputs/7.txt') as file:
    raw = file.read()
bags = make_bags(raw)
tot = tot_eventual_bags(bags, 'shiny_gold')
print('part1', tot)

# part 2

with open('inputs/7.txt') as file:
    raw = file.read()
bags = make_bags(raw)
starting_bag = bags['shiny_gold']
tot = tot_contained_bags(bags, starting_bag)
print('part2', tot)
