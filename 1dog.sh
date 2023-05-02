#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

# num of tests
    for k in {1..17}
    do
        # echo $i
        # echo $(($j*50))
        # vr=$(($j*50))
        folder="fit/sheep_20vr_1dog_300vr"
        echo $folder
        python main.py 1 300 $folder
    done
    python get_metrics.py $folder

# loop though vr of dogs
for j in {7..8}
do
    # num of tests
    for k in {1..20}
    do
        # echo $i
        # echo $(($j*50))
        vr=$(($j*50))
        folder="fit/sheep_20vr_1dog_${vr}vr"
        echo $folder
        python main.py 1 $vr $folder
    done
    python get_metrics.py $folder
done