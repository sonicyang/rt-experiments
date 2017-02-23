#!/bin/bash

KERNEL=`uname -r`
BENCH=mctest.user
OUTPUT=output.cyc/$BENCH
mkdir -p $OUTPUT

./mctest &
cyclictest -mnq -p 90 -h 1000 -i 1000 -l 1000000 > $OUTPUT/$BENCH.cyc.out &
sleep 0.5
ps > $OUTPUT/$BENCH.ps
echo 10000000 > /tmp/motion/trigger
sleep 1
insmod /lib/modules/$KERNEL/extra/sched_profiler.ko
sleep 3
cat /proc/sched_profiler > $OUTPUT/$BENCH.prof
sleep 10
cat /tmp/motion/statistic_result > $OUTPUT/$BENCH.out
