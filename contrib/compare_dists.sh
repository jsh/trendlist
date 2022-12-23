#!/bin/bash -eu

base=11

for i in {2..7}; do
	echo == $i ==
	printf "stirling numbers: "; count_trends.py $i stirling
	printf "powers of $base: "; count_trends.py $i powers --base $base
	printf "random floats: "; count_trends.py $i random
	((k = i+1))
	printf "uphill, powers of $base: "; count_trends.py $k powers --base $base --reverse True
	printf "uphill, random floats: "; count_trends.py $k random --reverse True
done
