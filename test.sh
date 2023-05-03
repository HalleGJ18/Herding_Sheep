#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

for i in {4..7}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="ct/none/1dog_${vr}vr"
            echo $folder
            python main.py 1 $vr $folder 75 none
        done
        python get_metrics.py $folder
done

for i in {4..7}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="ct/none/3dog_${vr}vr"
            echo $folder
            python main.py 3 $vr $folder 75 none
        done
        python get_metrics.py $folder
done

for i in {4..7}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="ct/fog/1dog_${vr}vr"
            echo $folder
            python main.py 1 $vr $folder 75 f
        done
        python get_metrics.py $folder
done

for i in {4..7}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="ct/fog/3dog_${vr}vr"
            echo $folder
            python main.py 3 $vr $folder 75 f
        done
        python get_metrics.py $folder
done


for i in {4..7}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="ct/mud/1dog_${vr}vr"
            echo $folder
            python main.py 1 $vr $folder 75 m
        done
        python get_metrics.py $folder
done

for i in {4..7}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="ct/mud/3dog_${vr}vr"
            echo $folder
            python main.py 3 $vr $folder 75 m
        done
        python get_metrics.py $folder
done


for i in {4..7}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="ct/hedge/1dog_${vr}vr"
            echo $folder
            python main.py 1 $vr $folder 75 h
        done
        python get_metrics.py $folder
done

for i in {4..7}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="ct/hedge/3dog_${vr}vr"
            echo $folder
            python main.py 3 $vr $folder 75 h
        done
        python get_metrics.py $folder
done
