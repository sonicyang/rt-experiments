#!/bin/bash

mkdir -p output

#mctest
mkdir -p output/mctest

./mctest &
insmod /lib/modules/4.4.12-rt19/extra/sched_profiler.ko
echo 10000000 > /tmp/motion/trigger
sleep 10s
cat /tmp/motion/statistic_result > output/mctest/mctest.out
cat /proc/sched_profiler > output/mctest/mctest.prof
killall mctest
