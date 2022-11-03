"""Unit-test trendlist.simple."""

import random
from collections import deque
from typing import Union

from trendlist import Initializer, Number, Rotations, Trend, rands
from trendlist.simple import pows


def test_typing() -> None:
    """Defined type."""
    assert Number == Union[float, int]
    assert Initializer == Union[Number, "Trend"]


def test_pows_default_base() -> None:
    """Default base is 2."""
    n = 5
    assert list(pows(n)) == [2**i for i in range(n)]


def test_pows_base() -> None:
    """Base can be reset."""
    n = 5
    assert list(pows(n, base=5)) == [5**i for i in range(n)]


def test_pows_start() -> None:
    """List rotation successful."""
    n = 10
    s = list(pows(n))
    for i in range(n + 2):
        dq = deque(s)
        dq.rotate(-i)
        assert list(pows(n, start=i)) == list(dq)


def test_rands() -> None:
    """Random sequence generated correctly."""
    n = 1000
    random_list = list(rands(n))
    assert len(random_list) == n  # right length
    assert all([isinstance(elem, float) for elem in random_list])  # all floats
    assert all([0 <= elem < 1 for elem in random_list])  # all in right range
    assert len(set(random_list)) == len(random_list)  # no dups


def test_rand_seed() -> None:
    """Random lists with the same seed are identical."""
    n = 10
    seed = random.random()
    list_a = list(rands(n, seed=seed))
    list_b = list(rands(n, seed=seed))
    assert list_a == list_b


def test_rand_start() -> None:
    """Random list rotated."""
    n = 10
    seed = random.random()
    rands_n = list(rands(n, seed=seed))
    for i in range(n + 2):
        dq = deque(rands_n)
        dq.rotate(-i)
        assert list(rands(n, seed=seed, start=i)) == list(dq)


def test_rotations_init() -> None:
    """Rotations initialized correctly."""
    rots = Rotations()
    assert rots.start == 0
    assert rots.num_rots == 0
