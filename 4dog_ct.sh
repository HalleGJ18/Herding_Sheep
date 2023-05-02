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
    for k in {1..20}
    do
        # echo $i
        # echo $(($j*50))
        vr=$(($j*50))
        folder="ct/sheep_20vr_4dog_${vr}vr"
        echo $folder
        python main.py 4 $vr $folder
    done
    python get_metrics.py $folder
done