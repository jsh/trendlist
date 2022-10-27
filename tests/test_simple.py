"""Unit tests for trendlist.simple module."""

from copy import copy
from typing import Any, List, Union

import pytest

from trendlist import pows
from trendlist.simple import Number, NumList, print_trends

SEQ_LEN = 5


@pytest.fixture()
def increasing() -> NumList:
    """Monotonically increasing sequence."""
    return NumList(pows(SEQ_LEN))


@pytest.fixture()
def increasing_smaller(increasing) -> NumList:
    """Shorter monotonically increasing sequence."""
    inc = copy(increasing)
    smaller = slice(0, -1)
    return NumList(inc[smaller])


@pytest.fixture()
def increasing_tiny() -> NumList:
    """Just two."""
    return NumList([1, 2])


@pytest.fixture()
def decreasing(increasing) -> NumList:
    """Monotonically decreasing sequence."""
    decreasing = copy(increasing)
    decreasing.reverse()
    return NumList(decreasing)


@pytest.fixture()
def decreasing_tiny() -> NumList:
    """Just two."""
    return NumList([2, 1])


@pytest.fixture()
def rising(increasing) -> NumList:
    """Rising trend."""
    rising = copy(increasing)
    rising[0], rising[1] = rising[1], rising[0]  # swap first two elements
    return NumList(rising)


@pytest.fixture()
def falling(increasing) -> NumList:
    """Falling trend."""
    falling = copy(increasing)
    falling[0], falling[-1] = falling[-1], falling[0]  # swap first and last elements
    return NumList(falling)


@pytest.fixture()
def level() -> NumList:
    """Level list."""
    return NumList([1 for elem in range(SEQ_LEN)])


@pytest.fixture()
def two_trends(increasing, increasing_smaller) -> NumList:
    """Sequence with two trends."""
    two_trends = copy(increasing)
    two_trends += copy(increasing_smaller)
    return NumList(two_trends)


@pytest.fixture()
def incs(increasing, increasing_smaller, increasing_tiny) -> List[Any]:
    """Monotonically increasing lists."""
    return [increasing, increasing_smaller, increasing_tiny]


@pytest.fixture()
def not_incs(
    decreasing, decreasing_tiny, rising, falling, level, two_trends
) -> List[Any]:
    """Not monotonically increasing lists."""
    return [decreasing, decreasing_tiny, rising, falling, level, two_trends]


@pytest.fixture()
def trends(increasing, increasing_smaller, increasing_tiny, rising) -> List[Any]:
    """Rising trends."""
    return [increasing, increasing_smaller, increasing_tiny, rising]


@pytest.fixture()
def not_trends(decreasing, decreasing_tiny, falling, level, two_trends) -> List[Any]:
    """Not rising trends."""
    return [decreasing, decreasing_tiny, falling, level, two_trends]


def test_number_type() -> None:
    """Type Number is defined correctly."""
    assert Number == Union[int, float]


def test_bad_numlist_item() -> None:
    """Bad NumList item detected."""
    with pytest.raises(TypeError) as excerr:
        NumList([1, 2, "a"])
    assert str(excerr.value) == "Item must be number."


def test_is_mono_inc(incs, not_incs) -> None:
    """is_mono_inc() checks whether a sequence is monotonically increasing."""
    # for inc in increasing, increasing_tiny:
    for inc in incs:
        assert inc.is_mono_inc()
    for not_inc in not_incs:
        assert not not_inc.is_mono_inc()


def test_is_mono_inc2(incs, not_incs) -> None:
    """is_mono_inc2() checks whether a sequence is monotonically increasing."""
    for inc in incs:
        assert inc.is_mono_inc2()
    for not_inc in not_incs:
        assert not not_inc.is_mono_inc2()


def test_is_trend(trends, not_trends) -> None:
    """is_trend() checks whether a sequence is a trend."""
    for trend in trends:
        assert trend.is_trend()
    for not_trend in not_trends:
        assert not not_trend.is_trend()


def test_pfx_trend(increasing, rising, two_trends) -> None:
    """pfx_trend() finds the longest prefix trend in a sequence."""
    assert two_trends.pfx_trend() == increasing
    assert increasing.pfx_trend() == increasing
    assert rising.pfx_trend() == rising


def test_empty_pfx_trend(increasing, rising, two_trends) -> None:
    """Passing an empty list to pfx_trend returns empty list."""
    assert NumList().pfx_trend() == []


def test_trend_list(two_trends, increasing, increasing_smaller, decreasing) -> None:
    """trend_list() decomposes a sequence into a list of trends."""
    assert two_trends.trend_list() == [increasing, increasing_smaller]
    assert decreasing.trend_list() == [[elem] for elem in decreasing]
    assert increasing.trend_list() == [increasing]


def test_print_trends(capsys) -> None:  # TODO: make a decent test here
    """print_trends() decomposes into trend_list, then pretty-prints it."""
    print_trends(pows(3))
    captured = capsys.readouterr()
    assert captured.out == "[1.00,2.00,4.00]\n"
    print_trends(list(reversed(pows(3))))
    captured = capsys.readouterr()
    assert captured.out == "[4.00][2.00][1.00]\n"
