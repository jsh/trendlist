"""Define and manipulate trends."""
# pylint: disable=fixme

import collections
import operator
import random
from dataclasses import dataclass
from typing import Iterable, List, Optional, Union

# new static types
Number = Union[float, int]
Initializer = Union[Number, "Trend"]


def pows(n: int, base: int = 2, start: int = 0) -> Iterable:
    """List sequences of powers of the base.

    base permits specifying the base
    start permits returning the numbers in a different (rotated) order,
        e.g., start=3 will give the numbers in the order
        "3rd, 4th, ... nth, 0th, 1st, 2nd"
    """
    start = start % n  # in case start >= n
    left = [base**i for i in range(start, n)]
    right = [base**i for i in range(start)]
    return left + right


def rands(n: int, seed: float = None, start: int = 0) -> Iterable:
    """Generate sequences of random floats.

    Ignoring flake8 warning S311 about pseudo-random-number generators.
    I want a pseudo-random number generator!

    seed permits a reproduceable "random" sequence
    start permits yielding the numbers in a different (rotated) order,
        e.g., start=3 will give the numbers in the order
        "3rd, 4th, ... nth, 0th, 1st, 2nd"
    """
    random.seed(seed)
    start = start % n  # in case start >= n
    for _ in range(start):
        random.random()  # ignore first `start` numbers
    for _ in range(start, n):
        yield (random.random())
    random.seed(seed)  # go back to the beginning
    for _ in range(start):
        yield (random.random())
    random.seed()  # reset the random-number generator


@dataclass(order=True)
class Trend:
    """Represent a single trend.

    Attributes:
        mean: The trend's arithmetic mean
        length: The trend's length. (default: 1)

    Raises:
        TypeError: Length is not an int
        ValueError: Length is not positive

    """

    mean: Number
    length: int = 1

    def __post_init__(self) -> None:
        """Validate the object.

        Raises:
            TypeError: Length is not an int
            ValueError: Length is not positive

        """
        if not isinstance(self.mean, (int, float)):
            raise TypeError("mean must be number")
        if not isinstance(self.length, int):
            raise TypeError("length must be integer")
        if self.length <= 0:
            raise ValueError("length must be positive")

    def merge(self, other, reverse=False) -> Optional["Trend"]:
        """Merge a trend into the current trend."""
        if self.mean == other.mean:
            raise ValueError("merging trend mean must differ!")
        can_merge = operator.gt if reverse else operator.lt
        if can_merge(self, other):
            length = self.length + other.length
            total = self.length * self.mean + other.length * other.mean
            mean = total / length
            return Trend(mean=mean, length=length)
        return None


class TrendList(list):
    """A list of trends.

    Note that this sub-classes list.
    """

    def __init__(
        self, s: Optional[List[Initializer]] = None, reverse: bool = False
    ) -> None:  # noqa: E501
        """Initialize Trend object."""
        if s is None:
            s = []
        for elem in s:
            if not isinstance(elem, Trend):  # accept either Trends or numbers
                elem = Trend(elem)
            self.append(elem)
        self._reverse = reverse

    def append(self, other: "Trend") -> None:
        """Append a new trend, in-place.

        Add a Trend into a TrendList.
        Merge with the rightmost Trend object,
        then continue recursively.
        """
        if not isinstance(other, Trend):
            raise TypeError("appended element must be Trend")
        if not self:
            super().append(other)
            return
        popped = self.pop()
        # if possible, merge and recurse
        if merged := popped.merge(other, reverse=self._reverse):
            self.append(merged)
        else:  # new trend cannot merge
            self.extend([popped, other])  # push popped back on, then other

    def rotate(self) -> "TrendList":
        """Move the leftmost trend to the right end, then merge."""
        merged = self
        if len(merged) > 1:
            left = merged[0]
            right = TrendList(merged[1:])
            right.append(left)
            merged = right
        return merged

    """
    After rotating a list, perhaps more than once,
    how many rotations did you do,
    and where, in the original list, was the current head?
    """
    Rotations = collections.namedtuple("Rotations", "start num_rots")

    def single(self) -> Rotations:
        """Rotate until there's a single trend."""
        new = self
        rotations = 0  # how many rotations to get to a single trend
        orig_start = 0  # position in original list that will become new[0]
        while len(new) > 1:
            orig_start += new[
                0
            ].len  # positon in self that will become new[0] following rotation
            new = new.rotate()
            rotations += 1
        return self.Rotations(start=orig_start, num_rots=rotations)
