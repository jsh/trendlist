#!/usr/bin/env python3
"""Average number of opposite trends, in a single trend of length N, is 2*ln(N)."""

import math
import random
import statistics

import fire
import matplotlib.pyplot as plt

import trendlist as tl
import trendlist.simple as tls


def count_opposite_trends(n):
    """Count opposite trends for sequence of length n.

    - Generate a random sequence.
    - Decompose into trends.
    - Rotate to single trend.
    - Regenerate rotated random sequence using the same seed.
    - Decompose into trends going the opposite direction.
    - Return number of opposite trends.
    """
    seed = random.random()  # random seed
    trends = tl.TrendList(tl.rands(n, seed))  # trendlist forward
    # where does single trend start?
    single = tl.rands(n, seed, trends.single().start)
    return len(tl.TrendList(single, reverse=True))  # count reverse trends


def ntrends(n, trials):
    """Count trends for given length.

    Return average count over multiple trials.
    """
    nt = []
    for _ in range(trials):
        nt.append(count_opposite_trends(n))
    return statistics.mean(nt)


def counts(points, trials):
    """Count trends for lengths that are powers of ten.

    Run several trials for each length.
    Plot the result.
    """
    counts = {}
    s_n = tls.pows(points, base=10)  # [1, 10, 100, ...]
    for i, n in enumerate(s_n):
        counts[i] = ntrends(n, trials)
    plt.scatter(counts.keys(), counts.values())
    plt.xlabel("log_10 length")
    plt.ylabel("number of opposite trends")
    plt.plot(
        range(points), [2 * math.log(elem) for elem in s_n], "g", label="y = 2*ln(x)"
    )
    plt.legend(loc="upper center")
    plt.show()


if __name__ == "__main__":
    fire.Fire(counts)
