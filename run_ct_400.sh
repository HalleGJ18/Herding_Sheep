#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

# test 400 vr

# loop through num of dogs
for i in 1 2 3 4 5
do
    for k in {1..15}
        do
            # echo $i
            # echo $(($j*50))
            # vr=$(($j*50))
            folder="ct/m/${i}dog/400vr"
            echo $folder
            python main_ct.py $i 400 $folder 75 m
        done
        python get_metrics.py $folder
done