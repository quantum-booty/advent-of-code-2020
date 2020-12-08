import re
from collections import defaultdict

import os
os.chdir(
    '/home/henryw/Documents/Study/Computer_Programming_for_Data_Scientists/advent-of-code-2020')

with open('inputs/8.txt', 'r') as file:
    raw = file.read()


def make_inst(raw):
    inst = []
    for line in raw.splitlines():
        op, arg = re.findall(r'(.{3}) (.\d+)', line)[0]
        # a smarter way would be to use op, arg = line.split()
        inst.append([op, int(arg)])
    return inst


def do_inst(op, arg, acc, i):
    if op == 'acc':
        return acc + arg, i + 1
    elif op == 'jmp':
        return acc, i + arg
    elif op == 'nop':
        return acc, i + 1


def get_acc_before_inf_loop(inst):
    acc = 0
    i = 0
    traversed = defaultdict(int)
    while True:
        op, arg = inst[i]
        traversed[i] += 1
        if traversed[i] == 2:
            return acc
        acc, i = do_inst(op, arg, acc, i)


# if an operation(line) is visited twice, it means there is an infinite loop.
# Part 1

test_raw = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

inst = make_inst(test_raw)
print('test 1', get_acc_before_inf_loop(inst))

inst = make_inst(raw)
print('part 1', get_acc_before_inf_loop(inst))

# Part 2


def swap_nop_jmp(inst, pos):
    new_inst = inst * 1
    op, arg = new_inst[pos]
    if op == 'jmp':
        op = 'nop'
    elif op == 'nop':
        op = 'jmp'
    new_inst[pos] = [op, arg]
    return new_inst


class Infinite_loop_exception(Exception):
    pass


def fix_inst(inst):
    for pos in [i if op in ['jmp', 'nop'] else None for i, (op, arg) in enumerate(inst)]:
        if pos is not None:
            new_inst = swap_nop_jmp(inst, pos)
            try:
                acc = 0
                i = 0
                traversed = defaultdict(int)
                while True:
                    op, arg = new_inst[i]
                    traversed[i] += 1
                    if traversed[i] == 2:
                        raise Infinite_loop_exception
                    acc, i = do_inst(op, arg, acc, i)
            except Infinite_loop_exception:
                pass
            except IndexError:
                # if there is no infinite loop the while true loop will try to
                # get index that does not exist in new inst.
                return acc


# If there is no infinite loop, every instruction is done at most once.

test_raw = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

inst = make_inst(test_raw)
print('test 2', fix_inst(inst))

inst = make_inst(raw)
print('part 2', fix_inst(inst))
