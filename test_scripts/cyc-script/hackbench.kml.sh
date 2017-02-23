#!/bin/bash

KERNEL=`uname -r`
BENCH=hackbench.kml
OUTPUT=$PWD/output.cyc/$BENCH
mkdir -p $OUTPUT

mkdir -p /trusted
cp `which cyclictest` /trusted/
hackbench -s 512 -l 1024 -P > $OUTPUT/$BENCH.out &
/trusted/cyclictest -mnq -p 90 -h 1000 -i 1000 -l 10000 > $OUTPUT/$BENCH.cyc.out &
ps > $OUTPUT/$BENCH.ps
sleep 1
insmod /lib/modules/$KERNEL/extra/sched_profiler.ko
sleep 3
cat /proc/sched_profiler > $OUTPUT/$BENCH.prof
fg
fg
