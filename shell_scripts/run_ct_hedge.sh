#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT
# h f empty
for e in h 
do
    i=4
    j=250
    folder="ct/${e}/${i}dog/${j}vr"
    echo $folder
    time python main_ct.py $i $j $folder 75 $e
    python get_metrics.py $folder

    # loop through num of dogs
    for i in 5
    do
        # loop though vr of dogs
        # 50 75 100 125 150 175 200 250 300 350 400
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