from typing import List, Optional, Tuple, Dict
import itertools
import heapq


class Node:
    def __init__(self, value: int, next: Optional['Node'] = None) -> None:
        self.value: int = value
        self.next: Optional['Node'] = next

    def __str__(self) -> str:
        return repr(self.value)


class Game:
    def __init__(self, cups: List[int]) -> None:
        self.head: Node
        # use hashing for quick access rather than searching through the nodes
        # from head.
        self.nodes: Dict[int, Node]
        self.build_game(cups)

        self.largest_4: List[int]
        self.smallest_4: List[int]
        self.set_smallest_largests_4()

        self.pickup: List[Node]

        # initialize the position at head
        self.cur_node = self.head

    def build_game(self, cups: List[int]) -> None:
        """set self.head and self.nodes"""
        self.head = Node(cups[0])
        self.nodes = {}
        self.nodes[cups[0]] = self.head
        node = self.head
        for cup in cups[1:]:
            node.next = Node(cup)
            node = node.next
            self.nodes[cup] = node

        assert node is not None
        node.next = self.head

    def set_smallest_largests_4(self) -> None:
        """Used for finding max and min node"""
        node_values = self.nodes.keys()
        self.largest_4 = heapq.nlargest(4, node_values)
        self.smallest_4 = heapq.nsmallest(4, node_values)

    def low_high_nodes(self, part1: bool = True) -> Tuple[Node, Node]:
        pickup_values = [node.value for node in self.pickup]
        largest_4 = self.largest_4[:]
        smallest_4 = self.smallest_4[:]

        for num in pickup_values:
            if num in largest_4:
                largest_4.remove(num)
            if num in smallest_4:
                smallest_4.remove(num)

        return self.nodes[min(smallest_4)], self.nodes[max(largest_4)]

    @staticmethod
    def traverse(text: str, head: Node, print_list=True) -> List[int]:
        nodes = []
        node = head
        seen = set()
        while True:
            if node.value in seen:
                break
            else:
                try:
                    assert node is not None
                    nodes.append(node)
                    seen.add(node.value)
                    node = node.next
                except Exception:
                    break
        nodes_values = [node.value for node in nodes]
        if print_list:
            print(text, nodes_values)
        return nodes_values

    def search(self, value: int, exclude_pickup: bool = True) -> Optional[Node]:
        if self.nodes[value]:
            if exclude_pickup:
                if not self.nodes[value] in self.pickup:
                    return self.nodes[value]
                else:
                    return None
            else:
                return self.nodes[value]
        else:
            return None

    def pop_3_after_cur(self) -> None:
        # delete pickups from self.head and set self.pickup
        cur_node = self.cur_node

        pickup_head = cur_node.next
        pickup_mid = pickup_head.next
        pickup_tail = pickup_mid.next

        self.pickup = [pickup_head, pickup_mid, pickup_tail]

        if self.head in self.pickup:
            # move the head if the head is picked up
            self.head = pickup_tail.next

        # delete the three nodes from the cups
        cur_node.next = pickup_tail.next
        # delete next of tail to isolate itself from the rest
        pickup_tail.next = None

    def play_round(self) -> None:
        self.pop_3_after_cur()
        pickup_head = self.pickup[0]
        pickup_tail = self.pickup[-1]

        lo_node, hi_node = self.low_high_nodes()

        dest_node = None

        for i in itertools.count(1):
            goal = self.cur_node.value - i
            if goal < lo_node.value:
                dest_node = hi_node
                break
            dest_node = self.search(goal)
            if dest_node:
                break

        pickup_tail.next = dest_node.next
        dest_node.next = pickup_head

        self.cur_node = self.cur_node.next
        self.pickup = []

    def play_n_rounds(self, n: int = 100) -> None:
        for i in range(n):
            self.play_round()
            if i % 1000 == 0:
                print(i / 1000)

    def part1(self) -> int:
        one_node = self.search(1, exclude_pickup=False)
        values = self.traverse('part1 answer', one_node, False)
        answer = ''.join([str(num) for num in values[1:]])
        return int(answer)

    def part2(self) -> int:
        one_node = self.search(1, exclude_pickup=False)
        assert one_node is not None
        return one_node.next.value * one_node.next.next.value


#
# Unit tests
#

TEST_RAW = [3, 8, 9, 1, 2, 5, 4, 6, 7]

RAW = [8, 5, 3, 1, 9, 2, 6, 4, 7]

game = Game(TEST_RAW)
game.play_n_rounds(10)
assert game.part1() == 92658374

game = Game(TEST_RAW)
game.play_n_rounds(100)
assert game.part1() == 67384529


def part2_raw(raw):
    return raw + [num for num in range(max(raw) + 1, 10**6 + 1)]


# game = Game(part2_raw(TEST_RAW))
# game.play_n_rounds(10 * 10**6)
# assert game.part2() == 149245887792

#
# Problem
#

game = Game(RAW)
game.play_n_rounds(100)
print('part1', game.part1())

game = Game(part2_raw(RAW))
game.play_n_rounds(10 * 10**6)
print(game.part2())
