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


def all_trendlists(seq):
    """Decompose *every* permutation of seq into trends."""
    return [trend_list(perm) for perm in perms(seq)]


def count_trends(trendlists, verbose=False):
    """Count the # of trends in each trendlist."""
    if verbose:
        for trendlist in trendlists:
            print(f"{trendlist=} has {len(trendlist)} trend(s)")
    return [len(trendlist) for trendlist in trendlists]


def trend_counts(trendlists):
    """Report how many permutations in trendlists have exactly k trends.

    Include 0 at the beginning to say that no permutation has *no* trends.
    Besides, Python programmers like the first array index to be 0, not 1.
    """
    s = trendlists[0]  # arbitrarily pick the first trendlist.
    n_bins = sum([len(elem) for elem in s])
    bins = [0] * (n_bins + 1)
    for ntrends, count in Counter(count_trends(trendlists)).items():
        bins[ntrends] = count
    return bins


def stirlings(n):
    """Compute n_trends() with Stirling numbers of the first kind."""
    row = []
    for k in range(n + 1):
        row.append(stirling(n=n, k=k, kind=1))
    return row


def single_trends(trendlists):
    """Return all single trends in trendlists."""
    singles = []
    for trendlist in trendlists:
        if len(trendlist) == 1:
            singles.append(trendlist[0])
    return singles


def sum_and_weighted_mean(counts):
    """Return the total and the weighted mean of a list."""
    tot = sum(counts)
    weighted_tot = 0
    for num, count in enumerate(counts):
        weighted_tot += num * count
    return (tot, weighted_tot / tot)


def uphills(trendlists):
    """Decompose single trends into uphill trends."""
    # pick out single trends
    singles = single_trends(trendlists)
    # reverse them, decompose, collect the decompositions
    _uphills = []
    for single in singles:
        single.reverse()
        uphill = trend_list(single)
        _uphills.append(uphill)
    return _uphills


def number_of_trends(length, mode, base=2, reverse=False, weird=1):
    """Report trends in sequences of given length.

    Three modes: 'stirling', 'random', and 'powers'.
    """
    if mode == "stirling":
        return str(stirlings(length))
    elif mode == "random":
        seq = rands(length)
    elif mode == "powers":
        seq = pows(length, base)
    elif mode == "weird":
        seq = pows(length, base)
        seq[length-1] *= weird
    else:
        return f"unknown mode '{mode}'"
    # generate the trendlists
    trendlists = all_trendlists(seq)
    if reverse:
        trendlists = uphills(trendlists)
    # report their sizes
    return str(trend_counts(trendlists))


if __name__ == "__main__":
    fire.Fire(number_of_trends)
