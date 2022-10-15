# Trendlist

This repository is source code for the *trendlist* project.
It builds the *trendlist* package, which includes the submodule *trendlist.simple*.

![Trends](2020_google_trends.png) <!--- https://imgs.xkcd.com/comics/2020_google_trends.png --->


## What are Trends?

### Background: Monotonic Sequences Are Well-Defined and Rare.

In a monotonically increasing sequence, every element is greater than the preceding element. They're sorted.
Monotonically decreasing sequences are steadily decreasing instead. They're sorted in reverse order.
Similarly, there are monotonically non-decreasing sequences, and monotonically non-increasing sequences.
Monotonic can mean any of these.

Some examples:

* monotonically increasing: 1, 2, 4, 8, 16, ...
* monotonically decreasing: -1, -3, -9, -27, ...
* monotonically non-decreasing: 1, 1, 2, 3, 5, 8, ...
* monotonically non-increasing: 1, 1, 1/2, 1/3, 1/5, 1/8, ...

For simplicity, let's focus on the monotonically increasing sequences, understanding that we can go back and reason analogously about the other three types.

Few real-world sequences are monotonic. For any sequence of *N*, random floats, only *1/N!* permutations are monotonically increasing,
though you could reasonably look at many of them and say they're generally getting bigger from one end to the other.

How can we relax monotonicity productively?

### Trends Are a Generalization of Monotonic Sequences.

Let's start with a different, but equivalent definition of monotonic.

If, for a sequence, **x_0, x_1, ..., x_n**,
every element in the subsequence **x_0, ..., x_k** is less than the every following element, **x_k+1, ... x_n**,
for all **0 < k < n**, then the sequence is monotonically increasing.

Or, simpler, if you put your finger between any two sequence elements, everything to the left of your finger is less than everything to the right.

Suppose, instead, when put your finger between any two sequence elements,
the *average* of everything to the left of your finger is less than the *average* of everything to the right.
Call that a trend.

In other words, a monotonic sequence is also a trend
but a trend doesn't have to be monotonic.

For example, **1, 2, 4, 8, 16** is both monotonic and a trend.
In contrast, **2, 1, 4, 8, 16** is not monotonic, yet it is a trend,
because **mean(2) = 2 < mean(1, 4, 8) = 13/3**,
**mean(2, 1) = 3/2 < mean(4, 8) = 6**.
and **mean(2, 1, 4) = 7/3 < mean(8) = 8**.

By convention, just as single number is a one-element, monotonically increasing sequence, it's also a one-element trend.

Not everything is a trend, but trends are far more common than monotonically increasing sequences,
and interesting in their own right.

### We Use the Arithmetic Mean for Averages

The easiest average to work with is the arithmetic mean,
but for defining trends, any average will work that satisfies one condition:
if S1 and S2 are sequences, and Average(S1) < Average(S2), then
Average(S1) < Average(S1 + S2) < Average(S2)

Geometric and harmonic means both satisfy this condition just as well as the arithmetic mean.  Modes do not. For example,

	mode(1, 1, 2, 2, 2) =  2; mode(1, 1, 3, 3, 3) = 3

but

	mode(1, 1, 2, 2, 2 + 1, 1, 3, 3, 3) =
	mode(1, 1, 1, 1, 2, 2, 2, 3, 3, 3) = 1

Right now, the code hard-wires "average" to "arithmetic mean."
Enhancing it, so the average to use could be specified in a config file, would be a useful upgrade.

### We Use Python Floats for Reals

If you're a mathematician, you can say things like, *"The probability that two random reals, independently chosen on a finite interval, are equal has Lebesgue measure zero."*
with a straight face.

This means that if you had a ***real*** random number generator, and generated a snotload of random floats, no two would ever be identical.

In Python, `random()` returns floats in `[0, 1)` that are random enough, and have enough digits,
that this module treats them like reals and pretends it'll never throw out duplicates.

The code nods to reality by throwing an exception if it notices a violation of this assumption.
It hasn't yet.

I'm assuming averages of two different random sequences of reals
are probably also never the same (again *"...Lebesgue measure zero"*),
but I would welcome a proof.

I believe the same about subsets of powers of primes -- that is, for any set of prime powers, `p**k`, differnt subsets have different means.
Again, this is an article of faith for which I don't yet have a formal proof.

### We Build Classes to Represent Trends and TrendLists

The submodule *trendlist.simple* represents trends as lists, and lists of trends as lists of lists.
This is a simple way to play with trends, but it's a pig.


If you tack two trends together, their combined average is a weighted average of the pair.
For example,
a rising trend with length **6** and mean **4.0**
followed by
a rising trend with length **2** and mean **8.0**,
will combine to form a single, rising trend of length **8**
and mean **(6*4.0 + 2*8.0)/8 = 40.0/8 = 5**.

Almost no operations with trends require storing
the actual, **x_i** values that make up the trend;
it's enough to keep track of the trend mean and trend length.
The trendlist package defines the class `Trend`, which only stores these two values,
and another class `Trendlist`, a subclass of `List`, which represents lists of `Trend`s.

### Trends Have Cool Properties

Any sequence breaks cleanly and uniquely into maximum-length, monotonically increasing subsequences. For example,

* [3, 1, 4, 1, 5, 9]  -> [[3], [1 4], [1 5 9]]

* [2, 7, 1, 8, 2, 8, 1, 8, 2, 8, 4, 5, 9, 0, 4, 5] -> [[2, 7], [1, 8], [2, 8], [1, 8], [2, 8], [4, 5, 9], [0, 4, 5]]

(We're letting single numbers be monotonic sequences, where needed, and we're excluding sequences with adjacent, repeating numbers, like [1, 1, 2, 3, 5, 8, 13])

The monotonic subsequences are called "ascents." They were investigated by Euler, who probably called them something else because he was German and wrote in Latin.

Notice a couple of things:

* The last number of an ascent is always greater than the first number of the next,

* Out of the N! permutations of a set of N numbers, only one -- the list after sorting -- is monotonically increasing.

Similarly, every sequence breaks cleanly and uniquely, into maximum-length trends.

* [3, 1, 4, 1, 5, 9]  -> [[3, 1, 4, 1, 5, 9]]

* [2, 7, 1, 8, 2, 8, 1, 8, 2, 8, 4, 5, 9, 0, 4, 5] -> [[2, 7, 1, 8, 2, 8, 1, 8, 2, 8, 4, 5, 9], [0, 4, 5]]

Here, we'll note that

- The means of the trends decrease monotonically. Every trend's mean is greater than the one to its right.

- Out of the N! permutations of a set of N numbers, (N-1)! are single trends.
Every sequence has exactly one circular permutation that's a single, increasing trend.

These perhaps-not-intuitively-obvious properties, along with many other cool things,
are shown in Ehrenfeucht, *et al. (vide infra)*.

### A Sketch of the Development Environment

I use `poetry` for environment and dependency management.
The file `pyproject.toml` contains specifications.

The code is linted with `isort` `black`, `flake8`, `mypy`, `bandit`, and `safety`, and tested with `pytest`.
The test suite is tested with `mutmut`.

Every one of these is documented at <https://readthedocs.io> under *toolname*.readthedocs.io .
except `safety`, which is documented at <https://pyup.io/safety>

I welcome suggestions on what other checks I should add.


### There's Plenty of Documentation

In addition to this README, the *trendlist* package is documented at `readthedocs.io`,
which also links to a repository full of tutorial notebooks, which are also available through `binder`.


## Reference
[Andrzej Ehrenfeucht, Jeffrey Haemer, and David Haussler Quasi-Monotonic Sequences: Theory, Algorithms and Applications. SIAM. J. on Algebraic and Discrete Methods 1987;8(3):410-429](https://scholar.colorado.edu/downloads/8049g581k)

+[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/jsh/trendlist)
