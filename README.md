# ELC2017: Effectively Measure and Reduce Kernel Latencies for Real-time Constraints

This document describe how to install patches we use on linux kernel 4.4 with preempt rt

# Grab our patches, configs, etc
Repo: https://github.com/sonicyang/ELC2017
Branch: ```master```

# Kernel
## Kernel 4.4 patched with PREEMPT_RT
Prepare a source directory of Linux Kernel 4.4 and patch it with PREEMPT_RT

There are kernel patches from mctest, wastedcores, and KML

### mctest
Repo: https://github.com/sonicyang/mctest
Branch: ```master```
In Directory: ```kernel_patches```

### WastedCores
Repo: https://github.com/sonicyang/wastedcores
Branch: ```master```
In Directory: ```patches```

### KML
Repo: https://github.com/sonicyang/KML
Branch: ```master```
In Directory: ```/```

We have updated the KML and Wasted-Cores patches to be compatiable with kernel 4.4.
These patches include Kernel-Mode-Linux, vDSO enahncement, the 4 bug-patches, profiler-patch and sanity checker patch.
Your can select and patch with the patches your want.

For running mctest, your would have to patch with patches in misc directory.
```
~/linux-source $ git am ../mctest/kernel_patches/misc/Set-kernel-module-constructor-as-default-enable.patch
~/linux-source $ git am ../mctest/kernel_patches/misc/Floating-point-support-for-kernel-module-constructor.patch
```

### Patching Procedures:
```bash
~/linux-source $ git apply <patch file>
```
Do this for every patches you want to include in your build.

Then, we tar the kernel up for building with buildroot.
```bash
~/linux-source $ cd ..
~ $ tar -cvf linux.tar linux-source --exclude='.git'
```

# Buildroot image
## Acquire the buildroot repo, we are using version: 2016.11
```bash
~ $ git clone git://git.buildroot.net/buildroot
~ $ cd buildroot
~/buildroot $ git checkout 2016.11
```

## Apply Patches to enable building the wastedcore tools, SystemTap, etc.
Procedure:
```bash
~/buildroot $ git apply ../ELC2017/buildroot_patches/*.patch
```

The first patch enable the ability to build systemtap
The second enable the ability to build the wastedcore tools, using code in this repo.

I have modified the profiler code as:
 - Enable changing the maxinum recording length and cpu count in buildroot menu.
 - Default:
    - Targeting 4 cores system
    - Shrink the max sched event entry size, total size should be 6 GB
 - Make these configable with CFLAGS 
     - -DNUM_CPU 
     - -DMAX_SAMPLE_ENTRIES

#### X86_64
```bash
~/buildroot $ cp ../ELC2017/buildroot_configs/x86_64-buildroot-config .config
~/buildroot $ cp ../ELC2017/kernel_configs/x86_64-kernel-config kconfig
```

#### ARM Cortex-A9 SOCFPGA
```bash
~/buildroot $ cp ../ELC2017/buildroot_configs/ARM-A9-buildroot-config .config
~/buildroot $ cp ../ELC2017/kernel_configs/ARM-A9-kernel-config kconfig
~/buildroot $ cp ../ELC2017/kernel_configs/vmalloc-384M.patch vmalloc-384M.patch
```

#### ARM Cortex-A9 SOCFPGA with KML
```bash
~/buildroot $ cp ../ELC2017/buildroot_configs/ARM-A9-KML-buildroot-config .config
~/buildroot $ cp ../ELC2017/kernel_configs/ARM-A9-KML-kernel-config kconfig
~/buildroot $ cp ../ELC2017/kernel_configs/vmalloc-384M.patch vmalloc-384M.patch
```

## Configs
### Buildroot config
buildroot config is enabled to build image with following packages:
 - rt-tools
 - lmbench
 - systemtap
 - wastecore tools and kernel modules
 - mctest : Coming Soon

```bash
~/buildroot $ make menuconfig # Navigate your self to the config entries
```
Adjust the CPU Number and Max Sample Entries according to your target platform in:
 - Target Packages
   - wastedcores

### Kernel config
Kernel config is set to be build with:
 - CONFIG_PREEMPT_RT_FULL

Wastedcore scheduler profiler requires CONFIG_SCHED_DEBUG, and CONFIG_SCHED_INFO
 - CONFIG_SCHED_DEBUG
 - CONFIG_SCHED_INFO

In KML Config, these are enabled:
 - CONFIG_KERNEL_MODE_LINUX=y
 - CONFIG_KML_CHECK_CHROOT=y
 - CONFIG_VDSO=y
 - CONFIG_ARM_LPAE=N

## Building Image
```bash
~/buildroot $ make
```
This will start the building process of target image.

mctest might fail to build. It's a bug. Build again without cleaning to over come this

#### KML user space mctest
```bash
# Coming Soon
```

# Install Image
## X86_64
Prepare an empty usb disk, the following procedure would erase any data on the drive.

We would dd the output image onto the usb drive, insert your drive and issue:
```bash
~/buildroot $ sudo dd if=output/images/disk.img of=/dev/sdx bs=4M
# change sdx according to the driver your using
```

After a while your driver should be ready for booting

## ARM Cortex A9 SOCFPGA
### Sign u-boot Image
SOCFPGA requies a signed u-boot. We will get and use mkpinage, made by `maximeh`, to sign it.

This tool require GO Lang to be presented on your system
```bash
~ $ sudo apt-get install golang
```

Get mkpimage source: https://github.com/maximeh/mkpimage
And build it.
```bash
~ $ git clone https://github.com/maximeh/mkpimage
~ $ cd mkpimage
~/mkpimage $ export GOPATH=$HOME/go 
~/mkpimage $ make
```

Sign the u-boot image:
```bash
~/buildroot/output/images $ ~/mkpimage/bin/mkpimage u-boot-spl.bin -o u-boot-spl-signed.bin
```

### Prepare SD Card
Create an SD card with following partitioning:
 - Partition 1: 500MB WinFAT(Id: b)
 - Partition 2: 1.5GB Linux(Id:83)
 - Partition 3: 10MB  Unknown(Id:a2)

Initialize FAT partition:
```bash
# Change sdx according to your drive in system
~/buildroot/output/images $ sudo mkdosfs /dev/sdx1
```

### Install Image to SD Card
Now we can dd the data onto the target SD Card
```bash
~/buildroot/output/images $ sudo dd if=u-boot-spl-signed.bin of=/dev/sdx3 bs=64k seek=0
~/buildroot/output/images $ sudo dd if=u-boot.img of=/dev/sdx3 bs=64k seek=4
~/buildroot/output/images $ sudo dd if=rootfs.ext2 of=/dev/sdx2 bs=64k
~/buildroot/output/images $ sudo mkdir /mnt/sdcard
~/buildroot/output/images $ sudo mount /dev/sdx1 /mnt/sdcard
~/buildroot/output/images $ sudo cp socfpga.dtb zImage /mnt/sdcard
~/buildroot/output/images $ sync;sync;sync
# Change sdx according to your drive in system
```

Your SD card should be ready to boot the Altera SOCFPGA Development Kit!

# Boot
Use the newly created driver/SD-Card to boot up the target system.

default user is ```root```, password is empty.

# Benchmarking
The testing script we used is located in test_scripts.

The target platform would need to be rebooted every time a test is executed.

# Plotting
First copy the result directory, either ouput or output.cyc, as plots/input
```
~/ELC2017/plots $ sudo cp -r /mnt/<drive>/root/output.cyc input
```

## Heat Map
Then, each test result's heat map can be ploted with:
```
~/ELC2017/plots $ ~/wastedcores/tools/visualizations_4.4/plots/generate_rows_sched_profiler.sh <BENCH NAME> <Start Second> <Highlighted CTX PID>
# e.g. ~/ELC2017/plots $ ./generate_rows_sched_profiler.sh hackbench.cyc 0 <pid of RT task>
```
Task running with <Highlighted CTX PID>'s CTX points will be blue, instead of yellow .

## Getting 1ms cyclictest's pid
The pid shown in ps command was the main task of cyclictest, not the RT task.
To find the RT task, we provided a simple script to find out the pid of tasks running with average of 1ms wakeup time in the profiled data.

First look into `input/<BENCH NAME>/<BENCH NAME>.ps`, find out the cyclictest main task's PID. 
We will use it as <BASE PID> to filter out other ~1ms tasks.

```
~/ELC2017/plots $ python get_cyc.py <BENCH NAME> <BASE PID>
# e.g. ~/ELC2017/plots $ python get_cyc.py hackbench.cyc 700
```

## Histogram and other graph for a single PID scheduling result
Requirements:
 - matplotlib

First get the cyclictest RT task PID using above method

Run the python plotters:
```
~/ELC2017/plots $ python plot_ctx.py <BENCH NAME> <PID>
~/ELC2017/plots $ python plot_cyc.py <BENCH NAME> <PID>
~/ELC2017/plots $ python plot_rq_enter.py <BENCH NAME> <PID>
```

Plotting result, produced by of any of the tool, would be in output/<BENCH NAME>/

# Acknowledgements
The patches of Wasted Cores is taken from github repo `jirka-h/wastedcores`
It's ported by user `jirka-h` from original author, `jplozi`'s repo `jplozi/wastedcores`, for supporting kernel 4.4.

The KML patches is originated from: http://web.yl.is.s.u-tokyo.ac.jp/~tosh/kml/, developed by: Toshiyuki Maeda
Been ported for kernel 4.4 by us.

Additional informations can be find in file, README.md, which is in each patches' directory.
