#!/bin/bash -eu

for i in {2..8}; do
	echo == $i ==
	count_trends.py $i stirling
	count_trends.py $i random
	count_trends.py $i powers 11
	((k = i+1))
	echo $i, $k
	count_trends.py $k powers 11 True
done
