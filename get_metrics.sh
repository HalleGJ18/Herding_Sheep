#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT
# h
for m in fit
do
  for e in empty
  do
      # loop through num of dogs
      for i in {1..5}
      do
        # loop though vr of dogs
        for j in 50 75 100 125 150 175 200 250 300 350 400
        do
        folder="${m}/${e}/${i}dog/${j}vr"
        echo $folder
        time python get_metrics.py $folder
        done
      done
  done
done