#!/usr/bin/env python3

from itertools import permutations
from sympy.combinatorics import Permutation as perm # break a single permutation into cycles


def c_print(s, reverse = False):
    ansi = "\x1b[1m" if reverse else "\x1b[0m"
    print(f"{ansi}{s}", end = "")

def print_cycles(cycles):
    for n, cycle in enumerate(cycles):
        c_print(cycle, reverse = n%2)
    c_print("\n")  # reset to normal

# putting it all together
def all_cycles(n):
    all_cycles = []
    for permutation in permutations(range(n)):
        all_cycles.extend(perm(permutation).full_cyclic_form)
    return all_cycles

def cycles_by_length(n):
    cycles = all_cycles(n)
    cycles_by_length = {}
    for length in (range(1, n+1)):
        cycles_by_length[length] = sorted([cycle for cycle in cycles if len(cycle) == length])
    return cycles_by_length

def cycle_block(n):
    cycle_block = []
    cbl = cycles_by_length(n)
    for length, list in cbl.items():
        cycle_block.append(["".join(map(str, cycle)) for cycle in list])
    return cycle_block

for cycle_length in cycle_block(4):
    print_cycles(cycle_length)
