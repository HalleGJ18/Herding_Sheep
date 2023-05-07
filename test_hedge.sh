#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT
# h
e=h

for k in {1..5}
do
    # echo $i
    # echo $(($j*50))
    # vr=$(($j*50))
    folder1="out/fit/${e}_1dog_100vr"
    echo $folder1
    python main_fit.py 1 100 $folder1 75 $e
    
    folder2="out/ct/${e}_1dog_400vr"
    echo $folder2
    python main_ct.py 1 400 $folder2 75 $e
done
python get_metrics.py $folder1
python get_metrics.py $folder2