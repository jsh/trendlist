"""Unit tests for class Trend."""

from math import e  # Euler's constant
from operator import ge, gt, le, lt

import pytest

from trendlist import Trend

VAL = e
TREND_STR = f"({VAL:.2f},1)"


@pytest.fixture(scope="module")
def test_trends() -> list:
    """Defind a standard list of test Trendlist.

    Used throughout test suite.
    """
    return [
        Trend(VAL),
        Trend(VAL, 1),
        Trend(mean=2 * VAL),
        Trend(length=2, mean=1.5 * VAL),
    ]


def test_init(test_trends: list[Trend]) -> None:
    """Test __init__()."""
    trend = test_trends[0]
    assert isinstance(trend, Trend)
    assert trend.mean == VAL
    assert trend.length == 1


def test_trend_default() -> None:
    """Default fields have expected values."""
    trend = Trend(mean=0)
    assert trend.length == 1
    with pytest.raises(ValueError, match="mean must be initialized"):
        trend = Trend(length=1)


def test_repr(test_trends: list[Trend]) -> None:
    """Test __repr__()."""
    assert repr(test_trends[0]) == "Trend(mean=2.718281828459045, length=1)"
    assert repr(test_trends[0]) == f"Trend(mean={e}, length=1)"


def test_str(test_trends: list[Trend]) -> None:
    """Test __str__()."""
    assert f"{test_trends[0]}" == TREND_STR
    assert str(test_trends[0]) == TREND_STR


def test_eq(test_trends: list[Trend]) -> None:
    """Test __eq__()."""
    assert test_trends[0] == test_trends[1]
    assert test_trends[1] != test_trends[2]


def test_lt(test_trends: list[Trend]) -> None:
    """Test dunder inequality functions."""
    assert test_trends[0] < test_trends[2]
    assert test_trends[2] > test_trends[0]
    assert not test_trends[0] < test_trends[0]
    assert not test_trends[0] > test_trends[0]
    assert test_trends[0] <= test_trends[1]  # ==
    assert test_trends[1] <= test_trends[2]  # <
    assert test_trends[0] >= test_trends[1]  # ==
    assert test_trends[2] >= test_trends[1]  # >


def test_bad_merge(test_trends: list[Trend]) -> None:
    """Test merge."""
    with pytest.raises(ValueError, match="merging trend mean must differ!") as excerr:
        test_trends[0].merge(test_trends[1])
    assert "merging trend mean must differ!" == str(excerr.value)


def test_merge(test_trends: list[Trend]) -> None:
    """Test merge."""
    merged_trend = test_trends[1].merge(test_trends[2])
    assert merged_trend == test_trends[3]


@pytest.mark.parametrize(
    "operator",
    [(ge), (gt), (le), (lt)],
)
def test_valid_compare(operator) -> None:
    """Defined compare operators are all supported."""
    trend1 = Trend(mean=1.0)
    with pytest.raises(TypeError) as excerr:
        operator(trend1, 5)
    assert "not supported" in str(excerr.value)


@pytest.mark.parametrize(
    ("exception_type", "mean", "length", "message"),
    [
        (ValueError, None, None, "mean must be initialized"),
        (ValueError, None, 1, "mean must be initialized"),
        (TypeError, e, e, "length must be integer"),
        (TypeError, [1, 2, 3], None, "mean must be number"),
        (TypeError, 1, e, "length must be integer"),
        (TypeError, 1, "a", "length must be integer"),
        (ValueError, 1, 0, "length must be positive"),
        (ValueError, 1, -1, "length must be positive"),
    ],
)
def test_trend_exception(
    exception_type,
    length: int,
    mean: float,
    message: str,  # TODO: static-type exception_type
) -> None:
    """Test error handling."""
    with pytest.raises(exception_type) as excerr:
        Trend(length=length, mean=mean)
    assert str(excerr.value) == message
