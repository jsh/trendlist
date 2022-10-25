"""Unit tests for trendlist.simple module."""

from copy import copy
from typing import List, Union

import pytest

from trendlist import pows
from trendlist.simple import (
    Number,
    is_mono_inc,
    is_mono_inc2,
    is_trend,
    pfx_trend,
    print_trends,
    trend_list,
)

SEQ_LEN = 5


@pytest.fixture()
def increasing() -> List:
    """Monotonically increasing sequence."""
    return pows(SEQ_LEN)


@pytest.fixture()
def increasing_smaller(increasing) -> List:
    """Shorter monotonically increasing sequence."""
    inc = copy(increasing)
    smaller = slice(0, -1)
    return inc[smaller]


@pytest.fixture()
def increasing_tiny() -> List:
    """Just two."""
    return [1, 2]


@pytest.fixture()
def decreasing(increasing) -> List:
    """Monotonically decreasing sequence."""
    decreasing = copy(increasing)
    decreasing.reverse()
    return decreasing


@pytest.fixture()
def decreasing_tiny() -> List:
    """Just two."""
    return [2, 1]


@pytest.fixture()
def rising(increasing) -> List:
    """Rising trend."""
    rising = copy(increasing)
    rising[0], rising[1] = rising[1], rising[0]  # swap first two elements
    return rising


@pytest.fixture()
def falling(increasing) -> List:
    """Falling trend."""
    falling = copy(increasing)
    falling[0], falling[-1] = falling[-1], falling[0]  # swap first and last elements
    return falling


@pytest.fixture()
def level() -> List:
    """Level list."""
    return [1 for elem in range(SEQ_LEN)]


@pytest.fixture()
def two_trends(increasing, increasing_smaller) -> List:
    """Sequence with two trends."""
    two_trends = copy(increasing)
    two_trends += copy(increasing_smaller)
    return two_trends


@pytest.fixture()
def incs(increasing, increasing_smaller, increasing_tiny) -> List:
    """Monotonically increasing lists."""
    return [increasing, increasing_smaller, increasing_tiny]


@pytest.fixture()
def not_incs(decreasing, decreasing_tiny, rising, falling, level, two_trends) -> List:
    """Not monotonically increasing lists."""
    return [decreasing, decreasing_tiny, rising, falling, level, two_trends]


@pytest.fixture()
def trends(increasing, increasing_smaller, increasing_tiny, rising) -> List:
    """Rising trends."""
    return [increasing, increasing_smaller, increasing_tiny, rising]


@pytest.fixture()
def not_trends(decreasing, decreasing_tiny, falling, level, two_trends) -> List:
    """Not rising trends."""
    return [decreasing, decreasing_tiny, falling, level, two_trends]


def test_number_type():
    """Type Number is defined correctly."""
    assert Number == Union[int, float]


def test_is_mono_inc(incs, not_incs) -> None:
    """is_mono_inc() checks whether a sequence is monotonically increasing."""
    # for inc in increasing, increasing_tiny:
    for inc in incs:
        assert is_mono_inc(inc)
    for not_inc in not_incs:
        assert not is_mono_inc(not_inc)


def test_is_mono_inc2(incs, not_incs) -> None:
    """is_mono_inc2() checks whether a sequence is monotonically increasing."""
    for inc in incs:
        assert is_mono_inc2(inc)
    for not_inc in not_incs:
        assert not is_mono_inc2(not_inc)


def test_is_trend(trends, not_trends) -> None:
    """is_trend() checks whether a sequence is a trend."""
    for trend in trends:
        assert is_trend(trend)
    for not_trend in not_trends:
        assert not is_trend(not_trend)


def test_pfx_trend(increasing, rising, two_trends) -> None:
    """pfx_trend() finds the longest prefix trend in a sequence."""
    assert pfx_trend(two_trends) == increasing
    assert pfx_trend(increasing) == increasing
    assert pfx_trend(rising) == rising


def test_empty_pfx_trend(increasing, rising, two_trends) -> None:
    """Passing an empty list to pfx_trend returns empty list."""
    assert pfx_trend([]) == []


def test_trend_list(two_trends, increasing, increasing_smaller, decreasing) -> None:
    """trend_list() decomposes a sequence into a list of trends."""
    assert trend_list(two_trends) == [increasing, increasing_smaller]
    assert trend_list(decreasing) == [[elem] for elem in decreasing]
    assert trend_list(increasing) == [increasing]


def test_print_trends(capsys) -> None:  # TODO: make a decent test here
    """print_trends() decomposes into trend_list, then pretty-prints it."""
    print_trends(pows(3))
    captured = capsys.readouterr()
    assert captured.out == "[1.00,2.00,4.00]"
    print_trends(list(reversed(pows(3))))
    captured = capsys.readouterr()
    assert captured.out == "[4.00][2.00][1.00]"
