"""Define and manipulate trends."""
# pylint: disable=fixme

from collections import namedtuple
from dataclasses import dataclass
import operator
import random
from typing import Iterable, Optional, Union

def pows(n: int, base: int = 2, start: int = 0) -> Iterable:
    """Generate sequences of powers of the base.
    base permits specifying the base
    start permits yielding the numbers in a different (rotated) order,
        e.g., start=3 will give the numbers in the order
        "3rd, 4th, ... nth, 0th, 1st, 2nd"
    """
    start = start % n # in case start >= n
    for i in range(start, n):
        yield base**i
    for i in range(start):
        yield base**i

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
    start = start % n         # in case start >= n
    for _ in range(start):
        random.random()       # ignore first `start` numbers
    for _ in range(start, n):
        yield(random.random())
    random.seed(seed)        # go back to the beginning
    for _ in range(start):
        yield(random.random())

@dataclass(order=True)
class Trend:
    """Represent a single trend.

    Attributes:
        mean: The trend's arithmetic mean
        length: The trend's length. (default: 1)

    Raises:
        TypeError: Length is not an int
        ValueError: Length is not positive

    TODO: write a post_init() to check for legit values in post_init
    """
    mean: Optional[int] = None
    length: int = 1

    def merge(self, other, reverse=False):
        can_merge = operator.gt if reverse else operator.lt
        if can_merge(self, other):
            length = self.length + other.length
            # weighted mean
            mean = (self.length*self.mean + other.length*other.mean)/length
            return Trend(mean=mean, length=length)
        return None

initializer = Union[float, int, "Trend"]

class TrendList(list):

    def __init__(self, s: list, reverse: bool = False):
        self._reverse = reverse
        for elem in s:
            if not isinstance(elem, Trend): # accept either bTrends or numbers
                elem = Trend(elem)
            self.append(elem)

    def append(self, other: "Trend"):
        """Append a new trend.

        Add a Trend into a TrendList.
        Merge with the rightmost Trend object,
        then continues recursively.
        """
        if not self:
            super().append(other)
            return
        popped = self.pop()
        if merged := popped.merge(other, reverse=self._reverse):  # merge and recurse
            self.append(merged)
        else:  # new trend cannot merge
            self.extend([popped, other])  # push popped back on, then other

    RotatedTrendList = namedtuple('RotatedTrendList', 'start rotations')

    def rotate(self):
        """Move the leftmost trend to the right end, then merge."""
        merged = self
        left = merged[0]
        right = TrendList(merged[1:])
        right.append(left)
        merged = right
        return merged
        
    def single(self):
        """Rotate until there's a single trend."""
        new = self
        rotations = 0   # how many rotations to get to a single trend
        orig_start = 0    # position in original list that will become new[0]
        while len(new) > 1:
            orig_start += new[0].len  # positon in self that will become new[0] following rotation
            new = new.rotate()
            rotations += 1
        rtl = RotatedTrendList(start = orig_start, rotations=rotations)
        return rtl
