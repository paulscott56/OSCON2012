#!/bin/bash
PYTHON=/usr/bin/python
function myprocess {
    $PYTHON georest.py > log.txt
}
NOW=$(date +"%b-%d-%y")

until myprocess; do
     echo "$NOW Server crashed. Restarting..." >> error.txt
     sleep 1
done
