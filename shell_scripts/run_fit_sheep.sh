#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

vr=75

# loop though num of sheep
for j in 125 
do
    for e in h
    do
        i=2
        for k in {1..8}
        do
            # echo $i
            # echo $(($j*50))
            # vr=$(($j*50))
            folder="${j}sheep/fit/${e}/${i}dog/${vr}vr"
            echo $folder
            time python main_fit.py $i $vr $folder $j $e
        done
        python get_metrics.py $folder
        # loop through num of dogs
        for i in {3..5}
        do
        # num of tests
            for k in {1..10}
            do
                # echo $i
                # echo $(($j*50))
                # vr=$(($j*50))
                folder="${j}sheep/fit/${e}/${i}dog/${vr}vr"
                echo $folder
                time python main_fit.py $i $vr $folder $j $e
            done
            python get_metrics.py $folder
        done
    done
done