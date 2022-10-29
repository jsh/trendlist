"""Trends as lists, trendlists as lists of lists.

This module lets you explore trends in sequences,
preserving all the information about the original sequences.
It works well enough for short sequences,
but is a real dog for sequences of lengths in the thousands.
"""

import statistics
from copy import copy
from typing import Iterable, Optional, Union

import blessed

Number = Union[int, float]


class NumList(list):
    """A list of numbers."""

    def __init__(self, s: Optional[Iterable] = None) -> None:  # noqa: E501
        """Initialize empty NumList object, or from an existing list.

        Args:
            s: Empty or a list

        Raises:
            TypeError: Some item in iterable not a number.
        """
        if not s:
            super().__init__()
        else:
            s = list(s)
            for elem in s:
                if not isinstance(elem, (int, float)):
                    raise TypeError("Item must be number.")
            super().__init__(s)

    def is_mono_inc(self) -> bool:
        """List is monotonically increasing.

        Returns:
            True iff the sequence is monotonically increasing.
        """
        s = self
        return all([s[i + 1] > s[i] for i in range(len(s) - 1)])

    def is_mono_inc2(self) -> bool:
        """List is monotonically increasing.

        There's more than one way to skin a cat.

        Returns:
            True iff the sequence is monotonically increasing.
        """
        s = self
        n = len(s)
        for i in range(1, n):
            if max(s[:i]) >= min(s[i:]):
                return False
        return True

    def is_trend(self) -> bool:
        """List is a trend.

        Returns:
            True iff the sequence is a trend.

        """
        s = self
        mean_s = statistics.mean(s)
        n = len(s)
        for i in range(1, n):
            if statistics.mean(s[:i]) >= mean_s:
                # prefix mean greater than the whole,
                # so greater than the suffix, too.
                return False
        return True  # every prefix mean is less than its suffix mean

    def pfx_trend(self) -> "NumList":
        """Return the first trend in the sequence.

        Returns:
            Longest prefix that is a trend.

        """
        s = copy(self)
        while s:  # start with the whole sequence
            if s.is_trend():  # work backwards until you find a trend
                return s
            s.pop()
        return s

    def trend_list(self) -> "NumLists":
        """Decompose a NumList into its trends.

        Returns:
            A list of the trends, each of which is a NumList.

        """
        s = self
        trend_list = NumLists()
        while s:
            p = s.pfx_trend()  # find the longest, leftmost trend
            trend_list.append(p)  # tack it onto the end of the trendlist
            s = NumList(s[len(p) :])  # decompose what remains  # noqa
        return trend_list


class NumLists(list):
    """A list containing NumList objects."""

    def __init__(self) -> None:  # noqa: E501
        """Initialize empty NumLists object."""
        super().__init__()

    def __str__(self) -> str:
        """Pretty, colored printout.

        Returns:
            Printable representation of the NumList objects.
        """
        term = blessed.Terminal()
        printable = ""
        for i, item in enumerate(self):
            trend_l = [f"{elem:0.2f}" for elem in item]
            trend_s = ",".join(trend_l)
            trend_p = "[" + trend_s + "]"
            printable += term.color(i)(trend_p)
        return printable


def print_trends(s: Iterable) -> None:
    """Decompose and pretty-print a sequence.

    Args:
        s: the sequence to decompose and pretty-print.

    """
    print(NumList(s).trend_list())
