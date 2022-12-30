#!/usr/bin/env python3
"""Decompose forward trends of specified length into reverse trends."""

import fire
from itertools import permutations
from trendlist import TrendList
from collections import Counter


def perm(permutation, base):
    """Return generator of powers of base for permutation."""
    return (base**k for k in permutation)


def trend_counts(length, forward=1, base=2):
    """Trend counts for uphill trends.

    Return count of uphill trends
    built on specified # of downhill trends.
    """
    lengths = []
    for permutation in permutations(range(length)):
        trends = TrendList(perm(permutation, base))
        if len(trends) == forward:
            rev = reversed(permutation)
            uphills = TrendList(perm(rev, base))
            lengths.append(len(uphills))
    counter = Counter(lengths)
    counts = [0]*(length+1)
    for key, value in counter.items():
        counts[key] = value
    return str(counts)


if __name__ == "__main__":
    fire.Fire(trend_counts)
