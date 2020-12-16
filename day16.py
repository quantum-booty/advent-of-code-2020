import re
from typing import List, NamedTuple, Tuple, Dict
from collections import defaultdict


class Rule(NamedTuple):
    field: str
    first: Tuple[int, int]
    second: Tuple[int, int]


Rules = List[Rule]
Ticket = List[int]
Tickets = List[Ticket]


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


def parse_tickets(tickets_raw: str) -> Tickets:
    tickets = []
    for ticket_raw in tickets_raw.split('\n')[1:]:
        if ticket_raw == '':
            continue
        ticket = [int(value) for value in ticket_raw.split(',')]
        tickets.append(ticket)
    return tickets


def parse_all(raw: str) -> Tuple[Rules, Ticket, Tickets]:
    rules_raw, my_ticket_raw, nearby_tickets_raw = raw.split('\n\n')
    rules = parse_rules(rules_raw)
    my_ticket = parse_tickets(my_ticket_raw)[0]
    nearby_tickets = parse_tickets(nearby_tickets_raw)
    return rules, my_ticket, nearby_tickets


def validate_rule(rule: Rule, value: int) -> bool:
    first = rule.first
    second = rule.second
    first_valid = min(first) <= value <= max(first)
    second_valid = min(second) <= value <= max(second)
    if first_valid or second_valid:
        return True
    else:
        return False


import numpy as np
import pandas as pd

Ticket_checklist = Dict[int, Dict[str, bool]]


def check_ticket2(rules: Rules, ticket: Ticket) -> Ticket_checklist:
    for i, value in enumerate(ticket):
        for j, rule in enumerate(rules):
            is_valid = validate_rule(rule, value)

    return None


def check_ticket(rules: Rules, ticket: Ticket) -> Ticket_checklist:
    ticket_checklist = dict()
    for value in ticket:
        field_validated = dict()
        for rule in rules:
            is_valid = validate_rule(rule, value)
            field_validated[rule.field] = is_valid
        ticket_checklist[value] = field_validated
    return ticket_checklist


def ticket_invalid_values(ticket_checklist: Ticket_checklist) -> List[int]:
    return [value for value in ticket_checklist if not any(ticket_checklist[value].values())]


def error_rate(raw: str) -> int:
    rules, my_ticket, nearby_tickets = parse_all(raw)
    ticket_scanning_error_rate = 0
    for ticket in nearby_tickets:
        ticket_checklist = check_ticket(rules, ticket)
        invalid_values = ticket_invalid_values(ticket_checklist)
        ticket_scanning_error_rate += sum(invalid_values)
    return ticket_scanning_error_rate


def identify_fields(rules: Rules, nearby_tickets: Tickets) -> List[List[str]]:
    # for each ticket, check if each position is valid
    # check if all the values are valid for a field in a position

    pos_checklist: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(lambda: 1))
    for ticket in nearby_tickets:
        ticket_checklist = check_ticket(rules, ticket)
        # Ticket_checklist = Dict[int, Dict[str, bool]]

        if ticket_invalid_values(ticket_checklist) != []:
            # skip invalid tickets
            continue

        for pos, field_checklist in enumerate(ticket_checklist.values()):
            for field in [rule.field for rule in rules]:
                pos_checklist[pos][field] *= field_checklist[field]

    identified_fields = [[field for field, is_valid in pos.items() if is_valid]
                         for pos in pos_checklist.values()]

    unique_fields = [set(fields) for fields in identified_fields]

    print('ayayay', [field for field in unique_fields if len(field) == 1])

    while True:
        prev_fields = unique_fields[:]
        for pos, field in enumerate(unique_fields):
            try:
                n_fields = set.union(*[field for field in unique_fields if len(field) == 1])
            except:
                break

            if field - n_fields == set():
                continue
            else:
                unique_fields[pos] -= n_fields

        if prev_fields == unique_fields:
            break

    # assert all(len(fields) == 1 for fields in unique_fields)

    return [list(field) for field in unique_fields]


def part2(raw: str) -> int:
    rules, my_ticket, nearby_tickets = parse_all(raw)
    identified_fields = identify_fields(rules, nearby_tickets)
    print(identified_fields)
    product = 1
    for pos, value in enumerate(my_ticket):
        if any('depart' in fields for fields in identified_fields[pos]):
            product *= value
    return product


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

# assert error_rate(TEST_RAW) == 71

with open('inputs/16.txt', 'r') as file:
    RAW = file.read()

print(error_rate(RAW))

TEST_RAW_2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

rules, my_ticket, nearby_tickets = parse_all(TEST_RAW_2)
fields = [list(field)[0] for field in identify_fields(rules, nearby_tickets)]
assert fields == ["row", "class", "seat"]

print(part2(TEST_RAW))
print(part2(RAW))
