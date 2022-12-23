#!/bin/bash -eu
# compare trend counts across distributions, regular and uphill, length $length
# distributions are
#     - powers of $base
#     - floats, U[0, 1)
# Stirling numbers of the first kind, S(length, k), are also printed, for comparison.
# Uphill distributions are built on single-trends in the opposite direction,
# and begin with single trends one element longer (for reasons that the output makes clear)

echo
echo "Trend Count Comparisons Across Distributions."
echo

max=${1:-6}  # maximum length (default to 6)
base=11

length=2 # start here
for (( length=2; length <= max; length += 1 )); do
	echo == $length ==
	printf "stirling numbers: "; count_trends.py $length stirling
	printf "powers of $base: "; count_trends.py $length powers --base $base
	printf "random floats: "; count_trends.py $length random
	((next = length+1))
	printf "uphill, length $next, powers of $base: "; count_trends.py $next powers --base $base --reverse True
	printf "uphill, length $next, random floats: "; count_trends.py $next random --reverse True
done
