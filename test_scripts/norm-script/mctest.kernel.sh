#!/bin/bash

mkdir -p output

#mctest
mkdir -p output/mctest.kernel

insmod ./mctest.ko
insmod /lib/modules/4.4.12-rt19/extra/sched_profiler.ko
echo 10000000 > /sys/devices/virtual/misc/motion-ctrl/experiment/trigger 
sleep 10s
cat /proc/sched_profiler > output/mctest.kernel/mctest.kernel.prof
