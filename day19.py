from typing import Dict, List
import re


class Rules:
    def __init__(self, raw: str, part2: bool = False) -> None:
        self.rules: Dict[str, str] = dict()
        self.messages: List[str] = []
        self.set_rules_messages(raw, part2)
        self.regex: str = self.set_regex(part2=part2)

    def set_rules_messages(self, raw: str, part2) -> None:
        """Populate self.rules with key: rule pairs.
        Also parse the messages into a list of strings."""
        rules_raw, messages_raw = raw.split('\n\n')

        # parse messages
        self.messages = [message for message in messages_raw.splitlines()]

        # parse rules
        for line in rules_raw.splitlines():
            key, rule_raw = line.split(':')
            self.rules[key] = rule_raw.strip()

        if part2:
            self.recursion_limit = 4
            self.recursion_count_8 = 0
            self.recursion_count_11 = 0
            self.rules['8'] = '42 | 42 8'
            self.rules['11'] = '42 31 | 42 11 31'
            self.rules['42'] = self.set_regex('42')
            self.rules['31'] = self.set_regex('31')

    class RecursiveLimit(Exception):
        pass

    def set_regex(self, key: str = '0', part2=False) -> str:
        """Parse through the rules and create the regex recursively."""
        rule = self.rules[key]
        if rule in ('"a"', '"b"'):
            return rule[1]
        else:
            try:
                if part2:
                    if key == '8':
                        if self.recursion_count_8 == self.recursion_limit:
                            raise RecursionError
                        else:
                            self.recursion_count_8 += 1
                    if key == '11':
                        if self.recursion_count_11 == self.recursion_limit:
                            raise RecursionError
                        else:
                            self.recursion_count_11 += 1

                child_keys = list(set(re.findall(r'(\d+)', rule)))
                child_keys.sort(reverse=True)
                if child_keys != []:
                    for child_key in child_keys:
                        child_regex = self.set_regex(child_key, part2)
                        rule = re.sub(f'\\b({child_key})\\b', child_regex, rule)

            except RecursionError:
                pass

            finally:
                return '(' + rule.replace(' ', '') + ')'

    def count_valid_messages(self) -> int:
        c = re.compile(self.regex)
        return sum(bool(c.fullmatch(message)) for message in self.messages)


#
# Unit tests
#

TEST_RAW_1 = '''0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

aab
aba
ayayaya'''

TEST_RAW_2 = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb'''

r = Rules(TEST_RAW_1)
assert r.count_valid_messages() == 2

r = Rules(TEST_RAW_2)
assert r.count_valid_messages() == 2

with open('inputs/19_part2_test.txt') as file:
    TEST_RAW_3 = file.read()

r = Rules(TEST_RAW_3)
assert r.count_valid_messages() == 3

r = Rules(TEST_RAW_3, part2=True)
assert r.count_valid_messages() == 12

#
# Problem
#
with open('inputs/19.txt') as file:
    RAW = file.read()

r = Rules(RAW)
# print(r.regex)
print(r.count_valid_messages())

r = Rules(RAW, part2=True)
print(r.regex)
print(r.count_valid_messages())
