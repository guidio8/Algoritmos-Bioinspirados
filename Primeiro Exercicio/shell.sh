#!/bin/bash

# Barbara - Out 2020 copiei dela

index=1
cat arguments.txt | while read line 
do
	n=1 #executa cada entrada 10x
	while [ $n -le 12 ]
	do
		echo "$(python3 tutorial1.py $line $n $index)"
		n=$(( n+1 )) #incrementa n
	done
	index=$(( index+1 )) #incrementa index da instancia
done
