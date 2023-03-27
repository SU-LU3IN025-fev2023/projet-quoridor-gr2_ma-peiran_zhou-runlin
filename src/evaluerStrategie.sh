#!/bin/bash
echo "tests for strategies starts !"

val=0
`rm -f dataStra1-5.txt`
while(( $val<20 ))
do
    `python3 main.py | tail -n 1 | grep -o "[0,1]" >> dataStra1-5.txt`
    val=$(($val+1))
done