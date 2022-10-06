import statistics
from copy import copy
from typing import List, Union

Number = Union[int, float]


def is_trend(s: List[Number]) -> bool:
    # the list, s, is a trend.
    mean_s = statistics.mean(s)
    for i in range(1, len(s)):
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
    return []


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
