#!/bin/bash

KERNEL=`uname -r`
BENCH=mctest.kernel
OUTPUT=$PWD/output.cyc/$BENCH
mkdir -p $OUTPUT

insmod ./mctest.ko
echo 10000000 > /sys/devices/virtual/misc/motion-ctrl/experiment/trigger 
cyclictest -mnq -p 90 -h 1000 -i 1000 -l 10000 > $OUTPUT/$BENCH.cyc.out &
ps > $OUTPUT/$BENCH.ps
sleep 1
insmod /lib/modules/$KERNEL/extra/sched_profiler.ko
sleep 3
cat /proc/sched_profiler > $OUTPUT/$BENCH.prof
fg
