#!/usr/bin/env python3
"""Average number of trends, in a sequence of length N, is ln(N)."""

import math
import statistics

import fire
import matplotlib.pyplot as plt

import trendlist as tl
import trendlist.simple as tls


def ntrends(n, trials):
    """Count trends for given length.

    Return average count over multiple trials.
    """
    nt = []
    for _ in range(trials):
        nt.append(len(tl.TrendList(tl.rands(n))))
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
    plt.ylabel("number of trends")
    plt.plot(range(points), [math.log(elem) for elem in s_n], "g", label="y = ln(x)")
    plt.legend(loc="upper center")
    plt.show()


if __name__ == "__main__":
    fire.Fire(counts)
