# 1) first be able to evaluate the expression without parenthesis
# 2) identify the nested parenthesis, the evaluate from the lowest level up
#    recursively until reaching a single integer

# The expression evaluates from left to right
# 1+3*2 = (1+3)*2 = 8

import re
from typing import List, Union, Callable

Question = List[str]
Homework = List[Question]


class Operation:
    def parse_operation(self, op_str: str):
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


def no_parenthesis_eval(line: str) -> str:
    q_list = re.split(r'(\d+)', line)
    if len(q_list) == 1:
        return q_list[0]

    else:
        if q_list[0] == '':
            q_list = q_list[1:]
        if q_list[-1] == '':
            q_list = q_list[:-1]

        q: Question = q_list

        operation = Operation()
        operation.parse_operation(q[1])
        result = operation.op(q[0], q[2])
        for pos, char in enumerate(q):
            if pos < 3:
                continue
            if pos % 2 == 1:
                # odd means the the char is an operator
                operation.parse_operation(char)
            elif pos % 2 == 0:
                result = operation.op(str(result), char)
        return result


def eval_question(raw_line: str) -> int:
    raw_line = raw_line.replace(' ', '').replace('(', '\n').replace(')', '\n')
    question = [line for line in raw_line.splitlines() if line != '']
    new_question = []
    for line_num, line in enumerate(question):
        if re.match(r'^\d.*\d$', line):
            result = no_parenthesis_eval(line)
            new_question.append(result)
        else:
            new_question.append(line)

    if len(new_question) == 1:
        return int(new_question[0])

    no_paren_line = []
    new_new_question = []
    for line in new_question:
        if line != '*' and line != '+':
            no_paren_line.append(line)

        else:
            if len(no_paren_line) == 1:
                no_paren_line.append(line)
            else:
                result = no_parenthesis_eval(''.join(no_paren_line))
                new_new_question.append(result)
                new_new_question.append(line)
                no_paren_line = []
    if len(no_paren_line) == 1:
        result = no_paren_line[0]
    else:
        result = no_parenthesis_eval(''.join(no_paren_line))
    new_new_question.append(result)
    if len(new_new_question) == 1:
        return int(new_new_question[0])
    final_result = no_parenthesis_eval(''.join(new_new_question))
    return int(final_result)


TEST_RAW_1 = """1 + 2 * 3 + 4 * 5 + 6"""
assert eval_question(TEST_RAW_1) == 71

TEST_RAW_2 = """1 + (2 * 3) + (4 * (5 + 6))"""
assert eval_question(TEST_RAW_2) == 51

TEST_RAW_3 = """2 * 3 + (4 * 5)"""
assert eval_question(TEST_RAW_3) == 26
TEST_RAW_4 = """5 + (8 * 3 + 9 + 3 * 4 * 3)"""
assert eval_question(TEST_RAW_4) == 437
TEST_RAW_5 = """5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"""
assert eval_question(TEST_RAW_5) == 12240
TEST_RAW_6 = """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""
assert eval_question(TEST_RAW_6) == 13632

with open('inputs/18.txt', 'r') as file:
    homework = file.read()

sum = 0
for i, question in enumerate(homework.splitlines()):
    print(i, question)
    sum += eval_question(question)
print(sum)
