#!/usr/bin/env python3
import itertools
import sys
from typing import Dict, List, Tuple  # type hinting
from sympy.combinatorics import Permutation
from collections import Counter
import math


def all_perms(n: int) -> List[Tuple[int]]:
    """All permutations of integers from 0 to n-1."""
    return list(itertools.permutations(range(0, n)))


def single_cycles(perms: List[Tuple[int]]) -> List[Tuple[int]]:
    """single cycles among permutations."""
    singles = []
    for perm in perms:
        if len(Permutation(perm).full_cyclic_form) == 1:
            singles.append(perm)
    return singles


def reversed_perms(perms: List[Tuple[int]]) -> List[Tuple[int]]:
    """reverse each cycle in cycle_list."""
    return [x[::-1] for x in perms]


def cycles_of_reversed_singles(n: int) -> List[List[List[int]]]:
    """reverse each cycle in cycle_list."""
    perms = all_perms(n)
    singles = single_cycles(perms)
    reversed_singles = reversed_perms(singles)
    reversed_cycles = []
    for perm in reversed_singles:
        reversed_cycles.append(Permutation(perm).full_cyclic_form)
    return reversed_cycles


def counts_of_element_lengths(elements: List[List]) -> Dict[int, int]:
    """count the number of lists of each length in l."""
    lengths = [len(element) for element in elements]
    counts = Counter(lengths)
    return counts

def uphill_cycle_counts(n: int) -> List[int]:
    """number of reversed cycles of length n."""
    rc = cycles_of_reversed_singles(n)
    count_dict = counts_of_element_lengths(rc)
    counts = [0] * n
    for key, value in count_dict.items():
        counts[key] = value
    return counts

def weighted_average(counts: List[int]) -> float:
    """weighted average of counts."""
    total = 0
    for i in range(len(counts)):
        total += i * counts[i]
    return total / sum(counts)
    

def main():
    """main function."""
    # print(all_perms(int(sys.argv[1])))
    # print(single_cycles(all_perms(int(sys.argv[1]))))
    # print(reversed_perms(single_cycles(all_perms(int(sys.argv[1])))))
    # print(cycles_of_reversed_singles(int(sys.argv[1])))
    #rc = cycles_of_reversed_singles(int(sys.argv[1]))
    #print(counts_of_element_lengths(rc))
    length = int(sys.argv[1])
    uhc_count = uphill_cycle_counts(length)
    print(weighted_average(uhc_count), math.log(length))



if __name__ == "__main__":
    main()
