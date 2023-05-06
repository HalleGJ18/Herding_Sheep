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
    for k in {1..20}
        do
            # echo $i
            # echo $(($j*50))
            # vr=$(($j*50))
            folder="fit/empty/${i}dog/400vr"
            echo $folder
            python main_fit.py $i 400 $folder 75 empty
        done
        python get_metrics.py $folder
done