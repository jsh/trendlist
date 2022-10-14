import statistics
from copy import copy
from typing import List, Union

Number = Union[int, float]


def is_mono_inc(s: List[Number]) -> bool:
    """True iff sequence is monotonically increasing."""
    return all([s[i+1] > s[i] for i in range(len(s) - 1)])


def is_mono_inc2(s: List[Number]) -> bool:
    """True iff sequence is monotonically increasing.
    
    There's more than one way to skin a cat.
    """
    n = len(s)
    for i in range(1, n):
        if max(s[:i]) > min(s[i:]):
            return False
    return True


def is_trend(s: List[Number]) -> bool:
    """The list, s, is a trend."""
    mean_s = statistics.mean(s)
    n = len(s)
    for i in range(1, n):
        if statistics.mean(s[:i]) > mean_s:
            # prefix mean greater than the whole,
            # so greater than the suffix, too.
            return False
    return True  # every prefix mean is less than its suffix mean


def pfx_trend(s: List[Number]) -> List[Number]:
    # Return the first trend in the sequence.
    t = copy(s)
    while t:  # start with the whole sequence
        if is_trend(t):  # work backwards until you find a trend
            return t
        t.pop()


def trend_list(s: List[Number]) -> List[List[Number]]:
    # Decompose a sequence into its trends,
    # return the list of trends.
    trend_list = []
    while s:
        p = pfx_trend(s)  # find the longest, leftmost trend
        trend_list.append(p)  # tack it onto the end of the trendlist
        p_len = len(p)
        s = s[p_len:]  # decompose what remains
    return trend_list


def print_trend_list(trendlist: List[List[Number]]) -> None:
    term = blessed.Terminal()
    for i, trend in enumerate(trendlist, start=1):
        trend_l = [f"{elem:0.2f}" for elem in trend]
        trend_s = ",".join(trend_l)
        trend_p = "[" + trend_s + "]"
        print(term.color(i)(trend_p), end="")
    print


def print_trends(s) -> None:
    tl = trendlist(s)
    print_trendlist(tl)
