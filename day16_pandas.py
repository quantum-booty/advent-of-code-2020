import re
from typing import List, NamedTuple, Tuple, Dict
from collections import defaultdict
import numpy as np
import pandas as pd


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


Pos = int
Ticket_checklist = Dict[Pos, Dict[str, bool]]


def check_ticket(rules: Rules, ticket: Ticket) -> Ticket_checklist:
    ticket_checklist = dict()
    for pos, value in enumerate(ticket):
        field_validated = dict()
        for rule in rules:
            is_valid = validate_rule(rule, value)
            field_validated[rule.field] = is_valid
        ticket_checklist[pos] = field_validated
    return ticket_checklist


def make_checklist_df(rules: Rules, nearby_tickets: Tickets) -> pd.DataFrame:
    dfs = []
    for ticket_num, ticket in enumerate(nearby_tickets):
        checklist = check_ticket(rules, ticket)
        checklist_df = pd.DataFrame(checklist).T
        checklist_df['value'] = ticket
        dfs.append(checklist_df)

    df = pd.concat(dfs, keys=np.arange(len(nearby_tickets)))
    df.index = df.index.set_names(['ticket_num', 'position'])
    return df


def validate_ticket(ticket_checklist: pd.DataFrame) -> int:
    """Returns the total invalid values in a ticket"""
    # row wise or
    columns_except_value = ticket_checklist.columns[ticket_checklist.columns != 'value']
    pos_is_valid = ticket_checklist[columns_except_value].sum(axis=1) > 0
    # the ~ operator invert a boolean array
    return ticket_checklist['value'][~pos_is_valid].sum()


def error_rate(raw) -> int:
    rules, my_ticket, nearby_tickets = parse_all(raw)
    checklist = make_checklist_df(rules, nearby_tickets)
    err_per_ticket = checklist.groupby(level=['ticket_num']).apply(validate_ticket)
    return err_per_ticket.sum()


def get_only_valid_checklist(checklist) -> pd.DataFrame:
    err_per_ticket = checklist.groupby(level=['ticket_num']).apply(validate_ticket)
    valid_ticket_nums = err_per_ticket.index[err_per_ticket == 0]
    valid_ticket_index = checklist.index.get_level_values(0).isin(valid_ticket_nums)
    return checklist[valid_ticket_index]


TEST_RAW_2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

# def identify_fields(raw: str) -> List[set]:
#     rules, my_ticket, nearby_tickets = parse_all(raw)
#     checklist = make_checklist_df(rules, nearby_tickets)
#     checklist = get_only_valid_checklist(checklist)
#     columns_except_value = checklist.columns[checklist.columns != 'value']
#     checklist = checklist[columns_except_value]

#     candidates: List[set] = []
#     for pos, ticket in (checklist.groupby('position').sum() == len(rules)).iterrows():
#         candidates.append(set(ticket.index[ticket]))

#     raise Exception
#     print(candidates)
#     while True:
#         prev_candidates = candidates[:]
#         for pos, fields in enumerate(candidates):
#             for one_field in [field for field in candidates if len(field) == 1]:
#                 if candidates[pos] == one_field:
#                     continue
#                 candidates[pos] -= one_field
#         if candidates == prev_candidates:
#             return candidates


def identify_fields(raw: str) -> List[set]:
    rules, my_ticket, nearby_tickets = parse_all(raw)
    checklist = make_checklist_df(rules, nearby_tickets)
    checklist = get_only_valid_checklist(checklist)
    num_valid_tickets = checklist.index.get_level_values(level=0).nunique()

    columns_except_value = checklist.columns[checklist.columns != 'value']
    checklist = checklist[columns_except_value]

    is_candidate = checklist.groupby('position').sum() == num_valid_tickets

    candidates: List[set] = []
    for pos, ticket in is_candidate.iterrows():
        candidates.append(set(ticket.index[ticket]))
    assert sum(fields != set() for fields in candidates) == len(candidates)
    while True:
        prev_candidates = candidates[:]
        for pos, fields in enumerate(candidates):
            for one_field in [field for field in candidates if len(field) == 1]:
                if candidates[pos] == one_field:
                    continue
                candidates[pos] -= one_field
        if candidates == prev_candidates:
            return candidates


# %%

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

assert error_rate(TEST_RAW) == 71

with open('inputs/16.txt', 'r') as file:
    RAW = file.read()

print(error_rate(RAW))
error_rate(RAW)

if False:
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
