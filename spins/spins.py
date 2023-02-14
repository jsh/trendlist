#!/usr/bin/env python3
import itertools
import sys
from typing import Dict, List, Tuple  # type hinting
from sympy.combinatorics import Permutation
from collections import Counter
import math
import fire


def all_perms(n: int) -> List[Tuple[int]]:
    """All permutations of integers from 0 to n-1."""
    return list(itertools.permutations(range(0, n)))

def spins(perm: Tuple[int]) -> List[Tuple[int]]:
    """All spins of a permutation."""
    spins = []
    for i in range(len(perm)):
        spins.append(perm[i:] + perm[:i])
    return spins


def single_cycles(perms: List[Tuple[int]]) -> List[Tuple[int]]:
    """single cycles among permutations."""
    singles = []
    for perm in perms:
        if len(Permutation(perm).full_cyclic_form) == 1:
            singles.append(perm)
    return singles


def counts_of_element_lengths(elements: List[List]) -> Dict[int, int]:
    """count the number of lists of each length in l."""
    lengths = [len(element) for element in elements]
    counts = Counter(lengths)
    return counts


def weighted_average(counts: List[int]) -> float:
    """weighted average of counts."""
    total = 0
    for i in range(len(counts)):
        total += i * counts[i]
    return total / sum(counts)
    

def main(n: int):
    """main function."""
    perms = all_perms(n)
    # perms = single_cycles(perms)
    for perm in perms:
        print(perm,"->", Permutation(perm).full_cyclic_form)
    return

    #print(counts_of_element_lengths(rc))



if __name__ == "__main__":
    fire.Fire(main)
