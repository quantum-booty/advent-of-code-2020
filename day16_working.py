import re
from typing import List, NamedTuple, Tuple, Set
import functools


class Rule(NamedTuple):
    name: str
    first: Tuple[int, int]
    second: Tuple[int, int]

    def validate(self, field: int) -> bool:
        first = self.first
        second = self.second
        first_valid = min(first) <= field <= max(first)
        second_valid = min(second) <= field <= max(second)
        if first_valid or second_valid:
            return True
        else:
            return False


Rules = List[Rule]
Ticket = List[int]
Tickets = List[Ticket]


class Validation:
    def __init__(self, raw: str) -> None:
        self.rules: Rules
        self.my_ticket: Ticket
        self.nearby_tickets: Tickets
        self.parse_all(raw)

    @staticmethod
    def parse_rules(rules_raw: str) -> Rules:
        rules = []
        for rule_raw in rules_raw.splitlines():
            matches = re.findall(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)', rule_raw)[0]
            assert len(matches) == 5
            field, first_lo, first_up, second_lo, second_up = matches
            first = (int(first_lo), int(first_up))
            second = (int(second_lo), int(second_up))
            rules.append(Rule(field, first, second))
        return rules

    @staticmethod
    def parse_tickets(tickets_raw: str) -> Tickets:
        tickets = []
        for ticket_raw in tickets_raw.split('\n')[1:]:
            if ticket_raw == '':
                continue
            ticket = [int(value) for value in ticket_raw.split(',')]
            tickets.append(ticket)
        return tickets

    def parse_all(self, raw: str) -> None:
        rules_raw, my_ticket_raw, nearby_tickets_raw = raw.split('\n\n')
        self.rules = self.parse_rules(rules_raw)
        self.my_ticket = self.parse_tickets(my_ticket_raw)[0]
        self.nearby_tickets = self.parse_tickets(nearby_tickets_raw)

    def check_ticket(self, ticket: Ticket) -> List[Set[str]]:
        return [{rule.name for rule in self.rules if rule.validate(field)} for field in ticket]

    @staticmethod
    def is_valid(checklist: List[Set[str]]) -> bool:
        return all(len(field_valid_rules) != 0 for field_valid_rules in checklist)

    def delete_invalid(self) -> None:
        self.nearby_tickets = [
            ticket for ticket in self.nearby_tickets if self.is_valid(self.check_ticket(ticket))
        ]

    def find_candidate_rules(self) -> List[Set[str]]:
        all_rule_names = {rule.name for rule in self.rules}
        checklists = [self.check_ticket(ticket) for ticket in self.nearby_tickets]
        all_candidates = [
            set.intersection(*[all_rule_names] + [checklist[i] for checklist in checklists])
            for i, field in enumerate(self.my_ticket)
        ]

        return all_candidates

    def identify_fields(self) -> List[str]:
        all_candidates = self.find_candidate_rules()

        while True:
            identified = [candidates for candidates in all_candidates if len(candidates) == 1]
            all_candidates = [
                candidates.difference(*identified) if candidates not in identified else candidates
                for candidates in all_candidates
            ]

            if len(all_candidates) == len(identified):
                break

        return [list(cand)[0] for cand in all_candidates]

    def part2(self) -> int:
        identified = self.identify_fields()
        departure_values = [
            field for field, name in zip(self.my_ticket, identified) if 'depart' in name
        ]
        return functools.reduce(lambda x, y: x * y, departure_values)


#
# Unit tests
#

TEST_RAW = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

val = Validation(TEST_RAW)

val.delete_invalid()

with open('inputs/16.txt', 'r') as file:
    RAW = file.read()

val = Validation(RAW)
val.delete_invalid()
# identified = val.identify_fields()
print(val.part2())
