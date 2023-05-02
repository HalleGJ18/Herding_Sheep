#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

# loop through num of dogs
for i in {1..17}
do
    # echo $i
    # echo $(($i*50))
    folder="fit/sheep_20vr_2dog_400vr"
    echo $folder
    python main.py 2 400 $folder
done
python get_metrics.py $folder