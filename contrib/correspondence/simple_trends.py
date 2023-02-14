#!/usr/bin/env python3
from itertools import permutations

from typing import List

from trendlist.simple import pows, trend_list

def ns_to_pows(ns: List[int], base: int = 2):
    return [base**n for n in ns]


def ns_to_trend(ns: List[int]):
    return trend_list(ns_to_pows(ns))

def cycles_to_trends(cycles: List[List[int]]):
    return [ns_to_trend(cycle) for cycle in cycles]

def main():
    for perm in permutations(pows(4)):to
        print(f"{perm} -> {trend_list(list(perm))}")



if __name__ == "__main__":
    main()
