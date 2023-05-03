#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

# loop though vr of dogs
for j in {4..8}
do
    # num of tests
    for k in {1..20}
    do
        # echo $i
        # echo $(($j*50))
        vr=$(($j*50))
        folder="ct/sheep_20vr_5dog_${vr}vr"
        echo $folder
        python main.py 5 $vr $folder 100
    done
    python get_metrics.py $folder
done

# loop though vr of dogs
# for j in {1..8}
# do
#     # num of tests
#     for k in {1..15}
#     do
#         # echo $i
#         # echo $(($j*50))
#         vr=$(($j*50))
#         folder="ct75/sheep_20vr_5dog_${vr}vr"
#         echo $folder
#         python main.py 5 $vr $folder 75
#     done
#     python get_metrics.py $folder
# done