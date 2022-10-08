"""Unit tests for trendlists."""
# Prevent complaints about fixtures.
#   pylint: disable=redefined-outer-name
# TODO: don't hardwire averages

from itertools import permutations
from math import e, pi, factorial
import statistics
from typing import List

import pytest

from trendlist import Trend, TrendList, pows

# N.B.,
#    Decomposing a sequence into a list of maximal upwards trends
#    will produce a list with monotonically decreasing averages!
#    (and vice-versa)


VAL = e
TREND_STR = f"({VAL:.1f},1)"


@pytest.fixture(scope="module")
def test_trends() -> List:
    """Defind a standard list of test Trendlist.

    Used throughout test suite.
    """
    return [
        Trend(VAL),
        Trend(VAL, 1),
        Trend(mean=2 * VAL),
        Trend(length=2, mean=1.5 * VAL),
    ]


def test_init_empty() -> None:
    """Create TrendList objects."""
    trends = TrendList()
    # no initializer returns empty list
    assert isinstance(trends, TrendList)
    assert not trends


def test_init_with_numbers() -> None:
    """Initialize with decreasing ints."""
    values = list(reversed(pows(3)))  # reversed returns use-once iterator
    trends = [Trend(value) for value in values]
    assert TrendList(values) == trends


def test_init_with_trends() -> None:
    """Initialize with decreasing trends."""
    values = list(reversed(pows(3)))
    trends = [Trend(value) for value in values]
    assert TrendList(trends) == trends


def test_init_with_reverse() -> None:
    """Initialize with decreasing ints."""
    values = pows(3)  # [1, 2, 4]
    rev_values = list(reversed(values))  # [4, 2, 1]
    trendlist = TrendList(rev_values)  # descending means: [(4,1),(2,1),(1,1)]
    rev_trendlist = TrendList(
        values, reverse=True
    )  # ascending means: [(1,1),(2,1),(4,1)]
    assert list(trendlist) == list(reversed(rev_trendlist))


def test_str() -> None:
    trends = TrendList([pi, e])
    assert f"{trends}" == "[(3.14,1),(2.72,1)]"


def test_simple_append() -> None:
    """Append with no merging."""
    gen = reversed(pows(4))
    start = next(gen)
    trends = TrendList([start])
    for elem in gen:
        trends.append(Trend(elem))
    assert trends == TrendList(reversed(pows(4)))


def test_fancy_append() -> None:
    """Append with a simple merge."""
    trends = TrendList([VAL])
    trends.append(Trend(2 * VAL))
    assert trends == TrendList([Trend(VAL * 1.5, length=2)])


def test_single() -> None:
    nelems = 4
    all_trends = []
    single_trends = []
    elems = pows(nelems)
    elems_mean = statistics.mean(elems)
    elems_length = nelems
    for perm in permutations(elems):
        trends = TrendList(perm)
        single_trend = trends.single().pop()
        assert single_trend.length == nelems
        assert single_tren.mean == elems.mean
