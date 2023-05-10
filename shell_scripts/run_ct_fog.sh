#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT
# h f empty
for e in f 
do
    i=2
    j=50
    folder="ct/${e}/${i}dog/${j}vr"
    python get_metrics.py $folder
    
    # loop through num of dogs
    for i in {3..5}
    do
        # loop though vr of dogs
        for j in 400 350 300 250 
        do
            # num of tests
            for k in {1..12}
            do
                # echo $i
                # echo $(($j*50))
                # vr=$(($j*50))
                folder="ct/${e}/${i}dog/${j}vr"
                echo $folder
                time python main_ct.py $i $j $folder 75 $e
            done
            python get_metrics.py $folder
        done
    done
done