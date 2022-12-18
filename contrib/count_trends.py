#!/usr/bin/env python3
"""Count trend lists three modes: stirling numbers, random floats, powers-of-10."""

import itertools
from collections import Counter

import fire
from sympy.functions.combinatorial.numbers import (
    stirling,  # package for symbolic computation
)

from trendlist import rands
from trendlist.simple import pows, trend_list


def perms(s):
    """List all the permutations of the elements of s.

    s can be any iterable
    """
    _perms = itertools.permutations(s)  # _perms generates tuples
    _perms = [list(perm) for perm in _perms]  # but lists are easier to work with
    return _perms


def all_trend_lists(seq, verbose=False):
    """Decompose *every* permutation of seq into trends."""
    return [trend_list(perm) for perm in perms(seq)]


def count_trends(list_of_trendlists, verbose=False):
    """Count the # of trends in each trendlist."""
    if verbose:
        for trendlist in list_of_trendlists:
            print(f"{trendlist=} has {len(trendlist)} trend(s)")
    return [len(trendlist) for trendlist in list_of_trendlists]


def n_trends(s):
    """Show how many permutations of s have exactly k trends.

    Include 0 at the beginning to say that no permutation has *no* trends.
    Besides, Python programmers like the first array index to be 0, not 1.
    """
    s = list(s)
    counts = [0] * (len(s) + 1)
    for ntrends, count in Counter(count_trends(all_trend_lists(s))).items():
        counts[ntrends] = count
    return counts


def stirlings(n):
    """Compute n_trends() with Stirling numbers of the first kind."""
    row = []
    for k in range(n + 1):
        row.append(stirling(n=n, k=k, kind=1))
    return row


def number_of_trends(length, mode):
    """Report trends in sequences of given length.

    Three modes: 'stirling', 'random', and 'powers'.
    """
    if mode == "stirling":
        return stirlings(length)
    elif mode == "random":
        return n_trends(rands(length))
    elif mode == "powers":
        return n_trends(pows(length))
    else:
        return f"unknown mode '{mode}'"


if __name__ == "__main__":
    fire.Fire(number_of_trends)
