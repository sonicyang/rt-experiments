#!/bin/bash

KERNEL=`uname -r`
BENCH=mctest.kml
OUTPUT=$PWD/output.cyc/$BENCH
mkdir -p $OUTPUT

mkdir -p /trusted
cp ./mctest /trusted/
cp `which cyclictest` /trusted/
/trusted/mctest &
echo 100000 > /tmp/motion/trigger
/trusted/cyclictest -mnq -p 90 -h 1000 -i 1000 -l 10000 > $OUTPUT/$BENCH.cyc.out &
ps > $OUTPUT/$BENCH.ps
sleep 1
insmod /lib/modules/$KERNEL/extra/sched_profiler.ko
sleep 3
cat /proc/sched_profiler > $OUTPUT/$BENCH.prof
sleep 15
cat /tmp/motion/statistic_result > $OUTPUT/$BENCH.out
