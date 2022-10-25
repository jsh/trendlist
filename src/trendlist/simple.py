"""Trends as lists, trendlists as lists of lists.

This module lets you explore trends in sequences,
preserving all the information about the original sequences.
It works well enough for short sequences,
but is a real dog for sequences of lengths in the thousands.
"""

import statistics
from copy import copy
from typing import List, Union

import blessed

Number = Union[int, float]


def is_mono_inc(s: List[Number]) -> bool:
    """Sequence is monotonically increasing.

    Args:
        s: the sequence to test

    Returns:
        True iff the sequence is monotonically increasing.
    """
    return all([s[i + 1] > s[i] for i in range(len(s) - 1)])


def is_mono_inc2(s: List[Number]) -> bool:
    """Sequence is monotonically increasing.

    There's more than one way to skin a cat.

    Args:
        s: the sequence to test

    Returns:
        True iff the sequence is monotonically increasing.
    """
    n = len(s)
    for i in range(1, n):
        if max(s[:i]) >= min(s[i:]):
            return False
    return True


def is_trend(s: List[Number]) -> bool:
    """List, s, is a trend.

    Args:
        s: the sequence to test

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


def pfx_trend(s: List[Number]) -> List[Number]:
    """Return the first trend in the sequence.

    Args:
        s: the sequence to test

    Returns:
        Longest prefix that is a trend.

    """
    t = copy(s)
    while t:  # start with the whole sequence
        if is_trend(t):  # work backwards until you find a trend
            return t
        t.pop()
    return t


def trend_list(s: List[Number]) -> List[List[Number]]:
    """Decompose a sequence into its trends, return the list of trends.

    Args:
        s: the sequence to decompose.

    Returns:
        A list of the trends, each of which is a list.

    """
    trend_list = []
    while s:
        p = pfx_trend(s)  # find the longest, leftmost trend
        trend_list.append(p)  # tack it onto the end of the trendlist
        s = s[len(p) :]  # decompose what remains  # noqa
    return trend_list


def print_trend_list(trendlist: List[List[Number]]) -> None:
    """Nice, colored printout of a trend_list.

    Args:
        trendlist: the list of trends to print, coloring each trend differently.

    """
    term = blessed.Terminal()
    for i, trend in enumerate(trendlist):
        trend_l = [f"{elem:0.2f}" for elem in trend]
        trend_s = ",".join(trend_l)
        trend_p = "[" + trend_s + "]"
        print(term.color(i)(trend_p), end="")
    print


def print_trends(s) -> None:
    """Decompose and pretty-print a sequence.

    Args:
        s: the sequence to decompose and pretty-print.

    """
    tl = trend_list(s)
    print_trend_list(tl)
