#!/bin/bash

mkdir -p output
mkdir -p output/stress

insmod /lib/modules/4.4.12-rt19/extra/sched_profiler.ko
stress --cpu 4 --io 2 --vm 2 --vm-bytes 128M --timeout 1s --verbose > output/stress/stress.out
cat /proc/sched_profiler > output/stress/stress.prof
