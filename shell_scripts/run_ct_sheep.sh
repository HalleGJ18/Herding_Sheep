#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

vr=400
i=2
j=100
e=h
for k in {1..6}
do
    # echo $i
    # echo $(($j*50))
    # vr=$(($j*50))
    folder="${j}sheep/ct/${e}/${i}dog/${vr}vr"
    echo $folder
    time python main_ct.py $i $vr $folder $j $e
done
python get_metrics.py $folder

for i in {3..5}
do
# num of tests
    for k in {1..10}
    do
        # echo $i
        # echo $(($j*50))
        # vr=$(($j*50))
        folder="${j}sheep/ct/${e}/${i}dog/${vr}vr"
        echo $folder
        time python main_ct.py $i $vr $folder $j $e
    done
    python get_metrics.py $folder
done


# loop though num of sheep
j=125
for e in empty m f h
do
    # loop through num of dogs
    for i in {1..5}
    do
    # num of tests
        for k in {1..10}
        do
            # echo $i
            # echo $(($j*50))
            # vr=$(($j*50))
            folder="${j}sheep/ct/${e}/${i}dog/${vr}vr"
            echo $folder
            time python main_ct.py $i $vr $folder $j $e
        done
        python get_metrics.py $folder
    done
done