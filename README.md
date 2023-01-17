[![Build Status](https://app.travis-ci.com/jsh/trendlist.svg?branch=master)](https://app.travis-ci.com/jsh/trendlist)
[![Coverage Status](https://coveralls.io/repos/github/jsh/trendlist/badge.svg?branch=master)](https://coveralls.io/github/jsh/trendlist?branch=master)
[![PyPI](https://img.shields.io/pypi/v/trendlist)](https://pypi.org/project/trendlist)
[![PyPI download month](https://img.shields.io/pypi/dm/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![Documentation Status](https://readthedocs.org/projects/trendlist/badge/?version=latest)](https://trendlist.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/jsh/trendlist/blob/master/LICENSE)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jsh/trendlist-notebooks/master)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/jsh/trendlist)


# The Trendlist Project

This repository is source code for the *Trendlist* project.
It builds the *trendlist* package, which includes the submodule *trendlist.simple*.

![Trends](2020_google_trends.png) <!--- https://imgs.xkcd.com/comics/2020_google_trends.png --->


## What are Trends?

### Background: Sorted Sequences Are Well-Defined and Rare.

If you sort a set of numbers, by default every element is greater than or equal to its neighbor to the left.
A math geek would call such a sequence *monotonic*.

Monotonic is a big category, and can mean any of these:

* strictly increasing: 1, 2, 4, 8, 16, ...
* strictly decreasing: -1, -3, -9, -27, ...
* monotonically increasing: 1, 1, 2, 3, 5, 8, ...
* monotonically decreasing: 1, 1, 1/2, 1/3, 1/5, 1/8, ...

For simplicity, let's focus on the first of these four,
understanding that we can go back and reason analogously about the other three types.

We'll stick to working with sequences without repeats,
so we can just use "sorted" and "monotonic" to mean
"sorted increasing with no repeats" and "strictly increasing,"
and save typing.

(We'll return to avoiding repeats in a minute. Bear with us.)

When we say "sequence," we mean "finite sequence." This is software,
not calculus.

Few real-world sequences are sorted, but lots get generally bigger from one end to the other.

Can we relax sorting in an interesting way?
Let's give it a shot.

### Trends Are a Generalization of Sorted Sequences.

Start with a different but equivalent definition of sorted.

With a sorted sequence, if you put your finger between any two sequence elements, everything to the left of your finger is less than everything to the right.

Suppose, instead, when put your finger between any two sequence elements,
the *average* of everything to the left of your finger is less than the *average* of everything to the right.

A mathematician would call that a *quasi-monotonically increasing sequence*.
Which is why we'll call it a *trend*.

Trends are a superset of sorted sequences:
that is, a sorted sequence is a trend
but a trend doesn't have to be sorted.

Though not everything is a trend,
trends are far more common than sorted sequences.

For example, `1, 2, 4, 8, 16` is both sorted and a trend,
but `2, 1, 4, 8, 16` is not sorted, yet it is a trend.

* `mean(2) = 2 < mean(1, 4, 8) = 13/3`
* `mean(2, 1) = 3/2 < mean(4, 8) = 6`
* `mean(2, 1, 4) = 7/3 < mean(8) = 8`

So are `4, 1, 2, 8, 16` and twenty-one other permutations of the set `{1, 2, 4, 8, 16}`


They're also interesting.

### We Use the Arithmetic Mean for Averages

The average most of us use for most things is the arithmetic mean: the sum divided by the number of elements.
`mean([1, 2, 4, 8]) = (1+2+4+8)/4 = 15/4`

For defining trends, any average will work that satisfies one condition:
if `S1` and `S2` are sequences, and `Average(S1) < Average(S2)`, then
`Average(S1) < Average(S1 + S2) < Average(S2)`.

Geometric and harmonic means both satisfy this condition, as do some other even-more-obscure measures of central tendency,
but right now, the `trendlist` package hard-wires "average" to "arithmetic mean."

**TODO: Enhancing *trendlist*,
so you can specify the average to use in a config file,
would be a useful upgrade.**


### We Use Python Floats for Reals

If you're a mathematician, you can say things like, *"The probability that two random reals, independently chosen on a finite interval, are equal has Lebesgue measure zero."*
with a straight face.

This means, "If you had a true random number generator, and generated a snotload of random reals, no two would ever be exactly the same."

In Python, `random()` returns floats in `[0, 1)` that are random enough, and have enough digits,
that this package treats them like reals and pretends it'll never throw out duplicates.

The code nods to reality by throwing an exception if it notices a violation of this assumption.
It hasn't yet.

**TODO: Specifying the random-number generator in a config file
would be a useful enhancement.**

### Two Utilities: rands() and powers()

The `trendlist` package supplies two utilities for convenience: `rands()`
which generates lists of random floats,
and `pows`, which returns lists of powers of two
(`[1, 2, 4, 8, ...]`).

Both are useful for writing code to explore and illustrate trends.

**TODO: I've assumed averages of two different random sequences of reals
are never the same. (*"...Lebesgue measure zero"*).
I would welcome a proof.**

**TODO: I believe the same about subsets of powers of primes.
Again, a proof would be nice.**


### We Build Classes to Represent Trends and TrendLists

The submodule *trendlist.simple* represents trends as lists, and lists of trends as lists of lists.
This is a simple, and instructive way to play with trends and trend-lists, but it's a pig.
It's not worth waiting for the module to decompose a sequence of a thousand random floats into a list of trends.

Instead, the *trendlist* module supplies a second, more efficient approach for bigger problems, built on a simple observation:
when you tack two trends together, their combined average is a weighted average of the pair.

For example,
a rising trend with length `6` and mean `4.0`
followed by
a rising trend with length `2` and mean `8.0`,
will combine to form a single, rising trend of length `8`
and mean `(6*4.0 + 2*8.0)/8 = 40.0/8 = 5`.

Almost no operations with trends require storing
the actual sequence elements that make up the trend;
it's enough to keep track of the trend mean and trend length.
The `trendlist` package defines `class Trend`, instances of which only store these two values.
A second class, `TrendList`, represents lists of `Trend` objects, subclassing `List`.

Simplifying in this way gives us back reasonable performance.
You can use these abstractions turn a sequence of a million random floats into a TrendList in a second or two.

### Trends Have Cool Properties

It's pretty obvious that any sequence without repeats breaks cleanly and uniquely into maximum-length, sorted subsequences. For example,

* `[3, 1, 4, 1, 5, 9]`  -> `[[3], [1 4], [1 5 9]]`

* `[2, 7, 1, 8, 2, 8, 1, 8, 2, 8, 4, 5, 9, 0, 4, 5]` -> `[[2, 7], [1, 8], [2, 8], [1, 8], [2, 8], [4, 5, 9], [0, 4, 5]]`

We're calling single numbers sorted sequences, where needed. Here again, we won't deal with adjacent, repeating numbers, like `[1, 1, 2, 3, 5, 8, 13]`

These subsequences are called "ascents," and were studied in depth by Euler who probably called them something else because he was German and wrote in Latin.

Notice a couple of things:

* The last number of an ascent is always greater than the first number of the next,

* Out of the `N!` permutations of a set of N numbers, only one -- the list after sorting -- is a single ascent.

Pleasantly, every sequence also breaks cleanly and uniquely into maximum-length trends.

* `[3, 1, 4, 1, 5, 9]`  -> `[[3, 1, 4, 1, 5, 9]]`

* `[2, 7, 1, 8, 2, 8, 1, 8, 2, 8, 4, 5, 9, 0, 4, 5]` -> `[[2, 7, 1, 8, 2, 8, 1, 8, 2, 8, 4, 5, 9], [0, 4, 5]]`

Spoiler alert:

- The means of the trends drop from left to right.
They're sorted in reverse order.

- Out of the `N!` permutations of a set of `N` numbers, `(N-1)!` are single trends.
In fact, every sequence has exactly one circular permutation that's a single, increasing trend.

These perhaps-not-intuitively-obvious properties, along with many other cool things,
are proved in Ehrenfeucht, *et al. (vide infra)*.

### A Sketch of the Development Environment

This project uses `poetry` for environment and dependency management.
The file `pyproject.toml` contains versions for the packages it imports or uses in development.

The code is linted with `isort` `black`, `flake8`, `mypy`, `bandit`, and `safety`, and tested with `pytest`. 
The test suite provides 100% code coverage, and is, itself, mutation tested with `mutmut`.
Besides versions, the configuration, settings, and plugins for tools are defined in `pyproject.toml`.

The tools themselves are documented at <https://readthedocs.io> under *toolname*.readthedocs.io ,
except `safety`, which is documented at <https://pyup.io/safety>

**TODO: I'd welcome suggestions on what other checks I should add.**


### There's Plenty of Documentation

In addition to this README, the *trendlist* package is documented at [`readthedocs.io`](https://trendlist.readthedocs.io/en/latest/index.html).

There is [a repository of jupyter-notebook tutorials](https://github.com/jsh/trendlist-notebooks),
which you can clone yourself or bring up in [a binder container](https://mybinder.org/v2/gh/jsh/trendlist-notebooks.git/HEAD) either through the link here, or by clicking on the `binder` badge in the GitHub repository.

There are even [slides for a talk.](https://docs.google.com/presentation/d/1VAroX0kamfHWKFJHpvJrCJiZIOeOytO47s1XlfDryvE/edit#slide=id.p)


## Reference
[Andrzej Ehrenfeucht, Jeffrey Haemer, and David Haussler Quasi-Monotonic Sequences: Theory, Algorithms and Applications. SIAM. J. on Algebraic and Discrete Methods 1987;8(3):410-429](https://scholar.colorado.edu/downloads/8049g581k)
