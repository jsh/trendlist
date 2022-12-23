#!/bin/bash -eu
# compare uphill trend counts for different distributions
#     - powers of $base
# uphill distributions are built on single-trends in the opposite direction.
# Stirling numbers of the first kind, S(n, k), are also printed for n = length-1

echo
echo "Trend Count Comparisons, Sequences of length n, All Permutations of {p^k}, 0<=k<=n."
echo

max=${1:-6}  # maximum length (default to 6)
base=11

length=2 # start here
for (( length=2; length <= max; length += 1 )); do
    echo == length: $length ==
    for base in 2 3 5 7 11 13; do
        printf "uphill, powers of $base: "; count_trends.py $length powers --base $base --reverse True
    done
    ((prev = length-1))
    printf "stirling numbers, length $prev: "; count_trends.py $prev stirling
done
