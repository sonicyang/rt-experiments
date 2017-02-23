#!/bin/bash

mkdir -p output
mkdir -p output/hackbench

insmod /lib/modules/4.4.12-rt19/extra/sched_profiler.ko
hackbench -s 256 -l 32 -P > output/hackbench/hackbench.out
cat /proc/sched_profiler > output/hackbench/hackbench.prof
