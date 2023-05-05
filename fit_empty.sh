#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

# finish 3dog 50vr
for k in {1..10}
do
    # echo $i
    # echo $(($j*50))
    # vr=$(($j*50))
    folder="fit/empty/3dog/50vr"
    echo $folder
    python main_fit.py 3 50 $folder 75 empty
done
python get_metrics.py $folder

# finish rest of 3dog
for j in 75 100 125 150 175 200 250 300 350
    do
        # num of tests
        for k in {1..20}
        do
            # echo $i
            # echo $(($j*50))
            # vr=$(($j*50))
            folder="fit/empty/${i}dog/${j}vr"
            echo $folder
            python main_fit.py $i $j $folder 75 empty
        done
        python get_metrics.py $folder
    done

# loop through num of dogs
for i in 4 5
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
            folder="fit/empty/${i}dog/${j}vr"
            echo $folder
            python main_fit.py $i $j $folder 75 empty
        done
        python get_metrics.py $folder
    done
done