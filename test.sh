#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

for k in {1..2}
    do
        # echo $i
        # echo $(($j*50))
        # vr=$(($j*50))
        folder="fit/sheep_20vr_1dog_250vr"
        echo $folder
        python main.py 1 250 $folder
    done
    python get_metrics.py $folder