#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

e=f

# loop through num of dogs
    for i in {1..5}
    do
        # loop though vr of dogs
        for j in 50 75 100 125 150 175 200 250 300 350
        do
            # num of tests
            for k in {1..20}
            do
                # echo $i
                # echo $(($j*50))
                # vr=$(($j*50))
                folder="fit/${e}/${i}dog/${j}vr"
                echo $folder
                python main.py $i $j $folder 75 $e
            done
            python get_metrics.py $folder
        done
    done