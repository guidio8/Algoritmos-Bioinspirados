#!/bin/bash

# Barbara - Out 2020 copiei dela

cat arguments.txt | while read line 
do
	echo "$(python3 tutorial4.py $line)"
done
