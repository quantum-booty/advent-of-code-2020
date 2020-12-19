from typing import Dict, List
import re


class Rules:
    def __init__(self, raw: str) -> None:
        self.rules: Dict[str, str] = dict()
        self.abkeys: Dict[str, str] = dict()
        self.regex: str = ''
        self.messages: List[str] = []
        self.set_rules_messages(raw)
        self.set_regex()

    def set_rules_messages(self, raw: str) -> None:
        rules_raw, messages_raw = raw.split('\n\n')
        self.messages = [message for message in messages_raw.splitlines()]

        for line in rules_raw.splitlines():
            key, rule_raw = line.split(':')
            rule_raw = rule_raw.strip()
            if rule_raw[1] in ('a', 'b'):
                self.abkeys[rule_raw[1]] = key
            else:
                self.rules[key] = rule_raw

        a_key = self.abkeys['a']
        b_key = self.abkeys['b']
        for key in self.rules:
            self.rules[key] = self.rules[key].replace(a_key, 'a').replace(b_key, 'b')

    def set_regex(self, key: str = '0'):
        regex = self.rules[key]
        keys = set(re.findall(r'(\d+)', regex))
        if keys != set():
            for key_new in keys:
                regex = regex.replace(key_new, f'({self.set_regex(key_new)})').replace(' ', '')
                if key == '0':
                    self.regex = '^' + regex + '$'
                    # self.regex = regex
            return regex
        else:
            return regex

    def count_valid_messages(self) -> int:
        compiled = re.compile(self.regex)
        return sum(1 if compiled.match(message) else 0 for message in self.messages)


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
print(r.regex)
assert r.count_valid_messages() == 2

r = Rules(TEST_RAW_2)
print(r.regex)
assert r.count_valid_messages() == 2

#
# Problem
#

with open('inputs/19.txt') as file:
    RAW = file.read()

r = Rules(RAW)
print(r.regex)
print(r.count_valid_messages())
