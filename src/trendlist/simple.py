"""Trends as lists, trendlists as lists of lists.

This module lets you explore trends in sequences,
preserving all the information about the original sequences.
It works well enough for short sequences,
but is a real dog for sequences of lengths in the thousands.
"""

import statistics
from copy import copy

import blessed

IntList = list[int]


def pows(n: int, base: int = 2, start: int = 0) -> IntList:
    """Return sequence of `n` powers of the base.

    `n` specifies how many ints in the returned list

    `base` permits specifying the base, for example, `base=5` returns `[5^0, ..., 5^(n-1)]`

    `start` permits returning the numbers in a different (rotated) order,
    for example, `start=3` will give the numbers in the order
    "3rd, 4th, ... nth, 0th, 1st, 2nd"

    Args:
        n: how many powers to return
        base: what base to use for the powers
        start: how many positions to rotate the sequence before starting

    Returns:
        IntList

    TODO: I don't think it's worth adding a "reverse" argument. Amiright?
    """
    start = start % n  # in case start >= n
    rng = list(range(start, n)) + list(range(start))
    return [base**power for power in rng]


def is_mono_inc(s: IntList) -> bool:
    """List is monotonically increasing.

    Args:
        s: the sequence to evaluate

    Returns:
        True iff the sequence is monotonically increasing.
    """
    return all([s[i + 1] > s[i] for i in range(len(s) - 1)])


def is_mono_inc2(s: IntList) -> bool:
    """List is monotonically increasing.

    There's more than one way to skin a cat.

    Args:
        s: the sequence to evaluate

    Returns:
        True iff the sequence is monotonically increasing.
    """
    n = len(s)
    for i in range(1, n):
        if max(s[:i]) >= min(s[i:]):
            return False
    return True


def is_trend(s: IntList) -> bool:
    """List is a trend.

    Args:
        s: the sequence to evaluate

    Returns:
        True iff the sequence is a trend.

    """
    mean_s = statistics.mean(s)
    n = len(s)
    for i in range(1, n):
        if statistics.mean(s[:i]) >= mean_s:
            # prefix mean greater than the whole,
            # so greater than the suffix, too.
            return False
    return True  # every prefix mean is less than its suffix mean


def pfx_trend(s: IntList) -> IntList:
    """Return the first trend in the sequence.

    Args:
        s: the sequence to find the prefix trend of.

    Returns:
        Longest prefix that is a trend.

    """
    p = copy(s)  # make this return a new copy
    while p:  # start with the whole sequence
        if is_trend(p):  # work backwards until you find a trend
            return p
        p.pop()
    return p


def trend_list(s: IntList) -> list[IntList]:
    """Decompose a IntList into its trends.

    Args:
        s: the sequence to decompose

    Returns:
        A list of the trends.

    """
    trend_list = []
    while s:
        p = pfx_trend(s)  # find the longest, leftmost trend
        trend_list.append(p)  # tack it onto the end of the trendlist
        s = s[len(p) :]  # decompose what remains  # noqa
    return trend_list


def print_trends(s: IntList) -> None:
    """Pretty, colored printout.

    Args:
        s: the sequence to decompose and pretty-print.
    """
    all_trends = trend_list(s)
    term = blessed.Terminal()
    printable = ""
    for i, item in enumerate(all_trends):
        trend_l = [f"{elem:0.2f}" for elem in item]
        trend_s = ",".join(trend_l)
        trend_p = "[" + trend_s + "]"
        printable += term.color(i)(trend_p)
    print(printable)
