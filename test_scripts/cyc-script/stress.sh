#!/bin/bash

KERNEL=`uname -r`
BENCH=stress
OUTPUT=$PWD/output.cyc/$BENCH
mkdir -p $OUTPUT

stress --cpu 4 --io 2 --vm 2 --vm-bytes 128M --timeout 10s --verbose > $OUTPUT/$BENCH.out &
cyclictest -mnq -p 90 -h 1000 -i 1000 -l 10000 > $OUTPUT/$BENCH.cyc.out &
ps > $OUTPUT/$BENCH.ps
sleep 1
insmod /lib/modules/$KERNEL/extra/sched_profiler.ko
sleep 3
cat /proc/sched_profiler > $OUTPUT/$BENCH.prof
fg
fg
