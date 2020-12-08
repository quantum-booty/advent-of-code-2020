import re
from typing import List, NamedTuple
from collections import defaultdict

test_raw = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


def make_inst(raw):
    inst = []
    for line in raw.splitlines():
        op, arg = re.findall(r'(.{3}) (.\d+)', line)[0]
        inst.append([op, int(arg)])
    return inst


def parse_inst(op, arg, acc, i):
    if op == 'acc':
        return acc + arg, i + 1
    elif op == 'jmp':
        return acc, i + arg
    elif op == 'nop':
        return acc, i + 1


def print_acc_before_inf_loop(inst):
    acc = 0
    i = 0
    traversed = defaultdict(int)
    while True:
        op, arg = inst[i]
        traversed[i] += 1
        if traversed[i] == 2:
            print(acc)
            break
        print(op, arg, acc)
        acc, i = parse_inst(op, arg, acc, i)


with open('inputs/8.txt', 'r') as file:
    raw = file.read()

# if an operation(line) is visited twice, it means there is an infinite loop.
# Part 1
inst = make_inst(raw)
print_acc_before_inf_loop(inst)

# %% Part 2
# If there is no infinite loop, every instruction is done exactly once.

inst = make_inst(test_raw)

test_raw = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

for pos in [i if op in ['jmp', 'nop'] else None for i, (op, arg) in enumerate(inst)]:
    if pos is not None:
        new_inst = inst * 1
        if new_inst[pos] == 'jmp':
            new_inst[pos][0] = 'nop'
        elif new_inst[pos] == 'nop':
            new_inst[pos][0] = 'jmp'
        print(new_inst)
        break

while True:
    try:
        acc = 0
        i = 0
        traversed = defaultdict(int)
        while True:
            op, arg = new_inst[i]
            traversed[i] += 1
            if traversed[i] == 2:
                raise Exception
            acc, i = parse_inst(op, arg, acc, i)
    except Exception:
        new_inst = swap_nop_jmp(inst, changed)
        pass
    else:
        print(acc)
        break
