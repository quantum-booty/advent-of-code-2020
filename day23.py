from typing import List, Optional, Tuple
import itertools


class Node:
    def __init__(self, value: int, next: Optional['Node'] = None) -> None:
        self.value: int = value
        self.next: Optional['Node'] = next

    def __str__(self) -> str:
        return repr(self.value)


class Game:
    def __init__(self, raw) -> None:
        self.head: Node
        self.build_game(raw)

        self.lowest: int = -1

        # initialize the position at head
        self.cur_node = self.head
        self.pickup: List[Node]

    def build_game(self, raw: str) -> None:
        cups = [int(num) for num in list(raw)]
        self.head = Node(cups[0])
        node = self.head
        for cup in cups[1:]:
            node.next = Node(cup)
            node = node.next

        assert node is not None
        node.next = self.head

    def search(self, value: int) -> Optional[Node]:
        node = self.head
        seen = set()
        while True:
            if node.value in seen:
                return None
            else:
                if node.value == value:
                    return node

                seen.add(node.value)
                assert node.next is not None
                node = node.next

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

    def pop_3_after_cur(self) -> None:
        # returns the head of the three popped nodes
        cur_node = self.cur_node

        pickup_head = cur_node.next
        pickup_mid = pickup_head.next
        pickup_tail = pickup_mid.next

        self.pickup = (pickup_head, pickup_mid, pickup_tail)

        if self.head in self.pickup:
            self.head = pickup_tail.next

        # delete the three nodes from the cups
        cur_node.next = pickup_tail.next
        # delete next of tail to isolate itself from the rest
        pickup_tail.next = None

    def low_high_nodes(self) -> Tuple[Node, Node]:
        highest = self.head
        lowest = self.head
        seen = set()
        node = self.head
        while True:
            if node in seen:
                return lowest, highest
            else:
                seen.add(node)

            node = node.next
            if node.value > highest.value:
                highest = node
            elif node.value < lowest.value:
                lowest = node
            else:
                pass

    def play_round(self) -> None:
        self.pop_3_after_cur()
        pickup_head = self.pickup[0]
        pickup_tail = self.pickup[-1]

        print('cur cup:', self.cur_node)
        print('pick up:', pickup_head.value, pickup_head.next.value, pickup_tail.value)
        self.traverse('after pickup', self.head)

        lo_node, hi_node = self.low_high_nodes()
        print('lo', lo_node.value, 'hi', hi_node.value)

        dest_node = None

        for i in itertools.count(1):
            goal = self.cur_node.value - i
            print('goal', goal)
            if goal < lo_node.value:
                dest_node = hi_node
                break
            dest_node = self.search(goal)
            print('ayayayaaaaaaaaaaaaaaaaaaaaaaa', dest_node)
            if dest_node:
                break
        print('destination:', dest_node.value)

        pickup_tail.next = dest_node.next
        dest_node.next = pickup_head
        # dest next
        # dest pickup_head _ pickup_tail next

        self.cur_node = self.cur_node.next

    def play_n_rounds(self, n: int = 100) -> None:
        for i in range(n):
            self.traverse('cups:', self.head)
            self.play_round()
            print('------------------------------------')

    def labels_after_1(self) -> int:
        one_node = self.search(1)
        values = self.traverse('part1 answer', one_node, False)
        answer = ''.join([str(num) for num in values[1:]])
        return int(answer)


#
# Unit tests
#

TEST_RAW = '389125467'

RAW = '853192647'

game = Game(TEST_RAW)
game.play_n_rounds(10)
assert game.labels_after_1() == 92658374

#game = Game(TEST_RAW)
#game.play_n_rounds(100)
#assert game.labels_after_1() == 67384529

    ##
    ## Problems
    ##

    #game = Game(RAW)
    #game.play_n_rounds(100)
    #print('part1', game.labels_after_1())
