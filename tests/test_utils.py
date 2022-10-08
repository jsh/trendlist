import random
from collections import deque
from typing import Union

from trendlist import Initializer, Number, Rotations, Trend, pows, rands


def test_typing() -> None:
    assert Number == Union[float, int]
    assert Initializer == Union[Number, "Trend"]


def test_pows_default_base() -> None:
    n = 5
    assert pows(n) == [2**i for i in range(n)]


def test_pows_base() -> None:
    n = 5
    assert pows(n, base=5) == [5**i for i in range(n)]


def test_pows_start() -> None:
    n = 10
    for i in range(n + 2):
        dq = deque(pows(n))
        dq.rotate(-i)
        assert pows(n, start=i) == list(dq)


def test_rands() -> None:
    n = 1000
    random_list = list(rands(n))
    assert len(random_list) == n  # right length
    assert all([isinstance(elem, float) for elem in random_list])  # all floats
    assert all([0 <= elem < 1 for elem in random_list])  # all in right range
    assert len(set(random_list)) == len(random_list)  # no dups


def test_rand_seed() -> None:
    n = 10
    seed = random.random()
    list_a = list(rands(n, seed=seed))
    list_b = list(rands(n, seed=seed))
    assert list_a == list_b


def test_rand_start() -> None:
    n = 10
    seed = random.random()
    rands_n = list(rands(n, seed=seed))
    for i in range(n + 2):
        dq = deque(rands_n)
        dq.rotate(-i)
        assert list(rands(n, seed=seed, start=i)) == list(dq)


def test_Rotations() -> None:
    rots = Rotations()
    assert rots.start == 0
    assert rots.num_rots == 0
