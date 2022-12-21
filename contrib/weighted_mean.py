#!/usr/bin/env python3

from math import log

import fire
from sympy.functions.combinatorial.numbers import (
    stirling,  # package for symbolic computation
)

def weighted_mean(seq):
    w_sum = 0.0
    for i, n in enumerate(seq):
        w_sum += i*n
    return float(w_sum/sum(seq))


def stirlings(n):
    """Compute n_trends() with Stirling numbers of the first kind."""
    row = []
    for k in range(n + 1):
        row.append(stirling(n=n, k=k, kind=1))
    return row

def mean_stirling(n):
    one_more = [0] + stirlings(n)
    print(stirlings(n), one_more)
    print(log(n), weighted_mean(stirlings(n)), weighted_mean(one_more))

fire.Fire(mean_stirling)
