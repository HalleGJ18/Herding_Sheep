#!/bin/bash

control_c() {
    kill $PID
    exit
}

trap control_c SIGINT

for i in {1..10}
do
    PID=$!
    python main.py 1 250 test_sheep_20vr_1dog_250vr
done

python get_metrics.py test_sheep_20vr_1dog_250vr