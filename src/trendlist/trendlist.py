"""Define and manipulate trends."""
# pylint: disable=fixme

import operator
import random
from dataclasses import dataclass
from typing import Generator, Iterable, Optional, Union

# new static types
Number = Union[float, int]
Initializer = Union[Number, "Trend"]


def rands(n: int, seed: float = None, start: int = 0) -> Generator[float, None, None]:
    """Generate sequence of `n` random floats.

    `seed` permits a reproduceable "random" sequence

    `start` permits yielding the numbers in a different (rotated) order,
    For example, `start=3` will give the numbers in the order
    "3rd, 4th, ... nth, 0th, 1st, 2nd"

    Args:
        n: how many floats to yield
        seed: where to start (random number generator seed)
        start: how many positions to rotate the sequence before starting

    Yields:
        Random floats [float_0, float_1, ... float_(n-1)] generated from the seed.

    Ignore flake8 warning S311 about pseudo-random-number generators.
    I *want* a pseudo-random number generator!
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


@dataclass
class Rotations:
    """Charactize rotated trendlist.

    Where the original start has rotated to,
    and how many rotations it took to get it there.
    """

    start: int = 0
    num_rots: int = 0


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

    mean: Optional[Number] = None  # throw ValueError if not initialized
    length: int = 1

    def __post_init__(self) -> None:
        """Validate the object.

        Raises:
            TypeError: Mean is not a number
            TypeError: Length is not an int
            ValueError: Length is not positive

        """
        if self.mean is None:
            raise ValueError("mean must be initialized")
        if not isinstance(self.mean, (int, float)):
            raise TypeError("mean must be number")
        if not isinstance(self.length, int):
            raise TypeError("length must be integer")
        if self.length < 1:
            raise ValueError("length must be positive")

    def __str__(self) -> str:
        """Convert to a nice string to display.

        Returns:
            The string "(mean, length)"

        """
        return f"({self.mean:.2f},{self.length})"

    def merge(self, other: "Trend", reverse=False) -> Optional["Trend"]:
        """Merge a trend into the current trend.

        Args:
            other: A trend
            reverse: Merge decreasing trends.

        Raises:
            ValueError: self and other have same means.

        Returns:
            The merged trends if a merge is possible, None if not.
        """
        if self.mean == other.mean:
            raise ValueError("merging trend mean must differ!")
        can_merge = operator.gt if reverse else operator.lt
        if can_merge(self, other):
            length = self.length + other.length
            total = self.length * self.mean + other.length * other.mean  # type: ignore
            mean = total / length
            return Trend(mean=mean, length=length)
        return None


class TrendList(list):
    """A list of trends.

    Note that this sub-classes list.
    """

    def __init__(
        self, s: Iterable[Initializer] = None, reverse: bool = False
    ) -> None:  # noqa: E501
        """Initialize Trend object.

        Args:
            s: A list of either numbers or of Trend objects
            reverse: Create a decreasing trend
        """
        if s is None:
            s = []
        self._reverse = reverse
        for elem in s:
            if not isinstance(elem, Trend):  # accept either Trends or numbers
                elem = Trend(elem)
            self.append(elem)

    def __str__(self) -> str:
        """Convert to a nice string to display.

        Returns:
            The string "(mean, length)"
        """
        to_string = [str(elem) for elem in self]
        return "[" + ",".join(to_string) + "]"

    def append(self, other: "Trend") -> None:
        """Append a new trend, in-place.

        Add a Trend into a TrendList.
        Merge with the rightmost Trend object,
        then continue recursively.

        Raises:
            TypeError: object being merged not a Trend

        Args:
            other: Trend object to stick on the right end
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
        """Move the leftmost trend to the right end, then merge.

        Returns:
            New trendlist after single, left-to-right rotation and required merge(s).
        """
        merged = self
        if len(merged) == 1:
            return self
        left = merged[0]
        right = TrendList(merged[1:])
        right.append(left)
        merged = right
        return merged

    def single(self) -> "Rotations":
        """Rotate until there's a single trend.

        After rotating a list, perhaps more than once,
        how many rotations did you do,
        and where, in the original list, was the current head?

        Returns:
            Rotations(rotations = # required for single trend, orig_start = where single trend start was in original list)
        """
        rotations = 0  # how many rotations to get to a single trend
        orig_start = 0  # position in original list that will become new[0]
        while len(self) > 1:
            assert len(self) != 1  # noqa, just here for mutmut :-(
            orig_start = (
                orig_start + self[0].length
            )  # position in self that will become new[0] following rotation
            self = self.rotate()
            rotations += 1
        return Rotations(start=orig_start, num_rots=rotations)
