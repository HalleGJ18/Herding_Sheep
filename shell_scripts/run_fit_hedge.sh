#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT
# h
e=h
i=5
j=150
folder="fit/${e}/${i}dog/${j}vr"
echo $folder
time python main_fit.py $i $j $folder 75 $e
python get_metrics.py $folder