#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

# loop through num of dogs
for i in {2..5}
do
    # loop though vr of dogs
    for j in {1..8}
    do
        # num of tests
        for k in {1..20}
        do
            # echo $i
            # echo $(($j*50))
            vr=$(($j*50))
            folder="fit/sheep_20vr_${i}dog_${vr}vr"
            echo $folder
            python main.py $i $vr $folder
        done
        python get_metrics.py $folder
    done
done