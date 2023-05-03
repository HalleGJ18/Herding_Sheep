#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

# loop though vr of dogs
for j in {1..8}
do
    # num of tests
    for k in {1..15}
    do
        # echo $i
        # echo $(($j*50))
        vr=$(($j*50))
        folder="ct75/sheep_20vr_1dog_${vr}vr"
        echo $folder
        python main.py 1 $vr $folder 75
    done
    python get_metrics.py $folder
done