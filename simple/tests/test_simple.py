from simple.trendlist import is_mono_inc, is_mono_inc2, is_trend, pfx_trend, trend_list
from trendlist import pows, rands

from typing import List
import pytest
from copy import copy

SEQ_LEN = 5

@pytest.fixture
def increasing() -> List:
    return pows(SEQ_LEN)

@pytest.fixture
def increasing_smaller(increasing) -> List:
    inc = copy(increasing)
    smaller = slice(0,-1)
    return inc[smaller]

@pytest.fixture
def decreasing(increasing) -> List:
    decreasing = copy(increasing)
    decreasing.reverse()
    return decreasing

@pytest.fixture
def rising(increasing) -> List:
    rising = copy(increasing)
    rising[0], rising[1] = rising[1], rising[0]  # swap first two elements
    return rising 

@pytest.fixture
def falling(increasing) -> List:
    falling = copy(increasing)
    falling[0], falling[-1] = falling[-1], falling[0]  # swap first and last elements
    return falling 

@pytest.fixture
def two_trends(increasing, increasing_smaller) -> List:
    two_trends = copy(increasing)
    two_trends += copy(increasing_smaller)
    return two_trends

def test_is_mono_inc(increasing, decreasing, rising, falling) -> None:
    assert is_mono_inc(increasing)
    for not_inc in decreasing, rising, falling:
        assert not is_mono_inc(not_inc)

def test_is_mono_inc2(increasing, decreasing, rising, falling) -> None:
    assert is_mono_inc2(increasing)
    for not_inc in decreasing, rising, falling:
        assert not is_mono_inc2(not_inc)

def test_is_trend(increasing, decreasing, rising, falling) -> None:
    for trend in increasing, rising:
        assert is_trend(trend)
    for not_trend in decreasing, falling:
        assert not is_trend(not_trend)

def test_pfx_trend(increasing, rising, two_trends) -> None:
    assert pfx_trend(two_trends) == increasing
    assert pfx_trend(increasing) == increasing
    assert pfx_trend(rising) == rising

def test_trend_list(two_trends, increasing, increasing_smaller, decreasing):
    assert trend_list(two_trends) == [increasing, increasing_smaller]
    assert trend_list(decreasing) == [[elem] for elem in decreasing]
    # assert trend_list(increasing) == [increasing]
