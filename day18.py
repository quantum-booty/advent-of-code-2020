# 1) first be able to evaluate the expression without parenthesis
# 2) identify the nested parenthesis, the evaluate from the lowest level up
#    recursively until reaching a single integer

# The expression evaluates from left to right
# 1+3*2 = (1+3)*2 = 8

import re
from typing import List


class Operation:
    # doing this for the sake of practicing OOP
    def parse_operation(self, op_str: str) -> None:
        if op_str == '*':
            self.op = self.times
        elif op_str == '+':
            self.op = self.add
        else:
            raise ValueError

    @staticmethod
    def times(a: str, b: str) -> str:
        return str(int(a) * int(b))

    @staticmethod
    def add(a: str, b: str) -> str:
        return str(int(a) + int(b))


def parse_question(line) -> List[str]:
    q = re.split(r'(\d+)', line)
    if q[0] == '':
        q = q[1:]
    if q[-1] == '':
        q = q[:-1]
    return q


def left_to_right_eval(line: str) -> str:
    q = parse_question(line)

    operation = Operation()
    operation.parse_operation(q[1])
    result = operation.op(q[0], q[2])
    for pos, char in enumerate(q):
        if pos < 3:
            continue
        if pos % 2 == 1:
            # odd means that the char is an operator
            operation.parse_operation(char)
        elif pos % 2 == 0:
            result = operation.op(str(result), char)
    return result


def add_before_times_eval(line: str) -> str:
    q = parse_question(line)
    prod = 1
    while True:
        for pos, char in enumerate(q):
            if char == '+':
                result = int(q[pos - 1]) + int(q[pos + 1])
                q = q[0:pos - 1] + [str(result)] + q[pos + 2:]
                break
        if '+' not in q:
            for num in q:
                if num != '*':
                    prod *= int(num)
            return str(prod)


EVALUATORS = {'ltr': left_to_right_eval, 'abt': add_before_times_eval}


def eval_question(question: str, method: str) -> int:
    question = question.replace(' ', '')
    while True:
        open_pos = None
        for pos, char in enumerate(question):
            if char == '(':
                open_pos = pos
            if open_pos is not None and char == ')':
                close_pos = pos
                # slicer excludes brackets
                no_paren_question = question[open_pos + 1:close_pos]
                result = EVALUATORS[method](no_paren_question)

                # slicer overwrites brackets
                question = question[:open_pos] + result + question[close_pos + 1:]
                break
        try:
            result = EVALUATORS[method](question)
            return int(result)
        except Exception:
            pass


#
# Unit tests
#

TEST_RAW_1 = """1 + 2 * 3 + 4 * 5 + 6"""
TEST_RAW_2 = """1 + (2 * 3) + (4 * (5 + 6))"""
TEST_RAW_3 = """2 * 3 + (4 * 5)"""
TEST_RAW_4 = """5 + (8 * 3 + 9 + 3 * 4 * 3)"""
TEST_RAW_5 = """5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"""
TEST_RAW_6 = """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

assert eval_question(TEST_RAW_1, method='ltr') == 71
assert eval_question(TEST_RAW_2, method='ltr') == 51
assert eval_question(TEST_RAW_3, method='ltr') == 26
assert eval_question(TEST_RAW_4, method='ltr') == 437
assert eval_question(TEST_RAW_5, method='ltr') == 12240
assert eval_question(TEST_RAW_6, method='ltr') == 13632

assert eval_question(TEST_RAW_1, method='abt') == 231
assert eval_question(TEST_RAW_2, method='abt') == 51
assert eval_question(TEST_RAW_3, method='abt') == 46
assert eval_question(TEST_RAW_4, method='abt') == 1445
assert eval_question(TEST_RAW_5, method='abt') == 669060
assert eval_question(TEST_RAW_6, method='abt') == 23340

#
# Problem
#

with open('inputs/18.txt', 'r') as file:
    homework = file.read()

sum = 0
for i, question in enumerate(homework.splitlines()):
    sum += eval_question(question, method='ltr')
print(sum)

sum = 0
for i, question in enumerate(homework.splitlines()):
    sum += eval_question(question, method='abt')
print(sum)
