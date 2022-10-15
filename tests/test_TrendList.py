"""Unit tests for class TrendList."""
#   TODO: fix mypy complaints about reversed()

import statistics
from collections import deque
from math import e, pi

import pytest

from trendlist import Rotations, Trend, TrendList, pows, rands

# N.B.,
#    Decomposing a sequence into a list of maximal upwards trends
#    will produce a list with monotonically decreasing averages!
#    (and vice-versa)


VAL = e


def test_init_empty() -> None:
    """Create TrendList objects."""
    trends = TrendList()
    # no initializer returns empty list
    assert isinstance(trends, TrendList)
    assert not trends


def test_init_with_numbers() -> None:
    """Initialize with increasing ints."""
    seq_length = 5
    seq = list(pows(seq_length))
    seq_mean = statistics.mean(seq)

    trends = TrendList(seq)
    assert len(trends) == 1
    tot_length = sum([elem.length for elem in trends])
    assert tot_length == seq_length
    tot_mean = sum([elem.length * elem.mean for elem in trends]) / tot_length
    assert seq_mean == pytest.approx(tot_mean)


def test_init_with_trends() -> None:
    """Initialize with decreasing trends."""
    values = list(reversed(pows(3)))
    list_of_trends = [Trend(value) for value in values]
    assert TrendList(list_of_trends) == TrendList(values)


def test_init_with_reverse() -> None:
    """Initialize with decreasing ints."""
    values = pows(3)  # [1, 2, 4]
    rev_values = list(reversed(values))  # [4, 2, 1]
    trends = TrendList(rev_values)  # descending means: [(4,1),(2,1),(1,1)]
    rev_trends = TrendList(values, reverse=True)  # ascending means: [(1,1),(2,1),(4,1)]
    assert list(trends) == list(reversed(rev_trends))


def test_str() -> None:
    """Function __str__() returns friendly representation."""
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


def test_append_err() -> None:
    """Append a non-trend."""
    trends = TrendList([VAL])
    with pytest.raises(TypeError) as excerr:
        trends.append(e)  # type: ignore
    assert str(excerr.value) == "appended element must be Trend"


def test_rotate():
    """Rotation drops trend number in expected way."""
    seq = []
    for i in range(10, 0, -1):
        trend = pows(i, base=5)  # a trend
        seq.extend(trend)  # with a smaller mean than the last
    trends = TrendList(seq)
    assert len(trends) == 10
    assert len(TrendList(seq).rotate()) == 1


def test_rotation_type() -> None:
    """Rotation has expected type."""
    rotations = TrendList(pows(5)).single()
    assert isinstance(rotations, Rotations)


def test_noop_rotate() -> None:
    """Sequence with one trend takes no rotations."""
    seq_length = 5
    seq = pows(seq_length)
    trend = TrendList(seq)
    assert trend.rotate() == trend


def test_one_rot() -> None:
    """Sequence with one trend takes no rotations."""
    seq_length = 5
    seq = pows(seq_length) + pows(seq_length - 1)
    trend = TrendList(seq)
    assert len(trend) == 2
    assert len(trend.rotate()) == 1


def test_mean_length_invariant() -> None:
    """Mean and length of TrendList are invariant after rotation."""
    seq_length = 5
    seq = list(rands(seq_length))
    seq_mean = statistics.mean(seq)

    trends = TrendList(seq)
    trends.rotate()
    rot_length = sum([elem.length for elem in trends])
    assert rot_length == seq_length
    rot_mean = sum([elem.length * elem.mean for elem in trends]) / rot_length
    assert seq_mean == pytest.approx(rot_mean)


def test_pos_single() -> None:
    """Expected start position of single trend is as expected."""
    n = 11
    for i in range(n + 1):
        dq = deque(pows(n))
        dq.rotate(i)
        rotation = TrendList(dq).single()
        assert rotation.start == i % n


def test_noop_single() -> None:
    """Sequence with one trend takes no rotations."""
    seq_length = 5
    seq = pows(seq_length)
    rotations = TrendList(seq).single()
    assert rotations.num_rots == 0
    assert rotations.start == 0


def test_one_rot_single() -> None:
    """Sequence with two trends takes one rotation."""
    seq_len = 5
    seq = list(pows(seq_len))
    seq.extend(pows(seq_len - 1))
    trends = TrendList(seq)
    rotations = trends.single()
    assert rotations.start == seq_len
    assert rotations.num_rots == 1


def test_two_rot_single() -> None:
    """Sequence that requires two rotations reports them."""
    seq = []
    for trend_len in range(6, 1, -1):
        seq += pows(trend_len)  # decreasing means each time, no merge
    trends = TrendList(seq)
    assert len(trends) == 5
    rotations = trends.single()
    assert rotations.num_rots == 2
