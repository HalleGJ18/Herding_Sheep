#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

for i in {1..5}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="fit/none/1dog_${vr}vr"
            echo $folder
            python main.py 1 $vr $folder 75 none
        done
        python get_metrics.py $folder
done

for i in {1..5}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="fit/none/3dog_${vr}vr"
            echo $folder
            python main.py 3 $vr $folder 75 none
        done
        python get_metrics.py $folder
done

for i in {1..5}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="fit/fog/1dog_${vr}vr"
            echo $folder
            python main.py 1 $vr $folder 75 f
        done
        python get_metrics.py $folder
done

for i in {1..5}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="fit/fog/3dog_${vr}vr"
            echo $folder
            python main.py 3 $vr $folder 75 f
        done
        python get_metrics.py $folder
done


for i in {1..5}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="fit/mud/1dog_${vr}vr"
            echo $folder
            python main.py 1 $vr $folder 75 m
        done
        python get_metrics.py $folder
done

for i in {1..5}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="fit/mud/3dog_${vr}vr"
            echo $folder
            python main.py 3 $vr $folder 75 m
        done
        python get_metrics.py $folder
done


for i in {1..5}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="fit/hedge/1dog_${vr}vr"
            echo $folder
            python main.py 1 $vr $folder 75 h
        done
        python get_metrics.py $folder
done

for i in {1..5}
do
    vr=$(($i*50))
    for j in {1..5}
        do
            folder="fit/hedge/3dog_${vr}vr"
            echo $folder
            python main.py 3 $vr $folder 75 h
        done
        python get_metrics.py $folder
done