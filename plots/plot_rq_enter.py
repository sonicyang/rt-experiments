import sys
import matplotlib.pyplot as plt

INPUT = "input/" + sys.argv[1] + "/" + sys.argv[1] + ".prof"
PID = int(sys.argv[2])
OUTPUT = "output/" + sys.argv[1]

RQ_CACHE = dict()
data = []

for line in open(INPUT,'r'):
    if line.find("RQ") > -1:
        info = line.split()
        time = int(info[12])
        cpu = int(info[15])
        amount = int(info[16])

        if cpu not in RQ_CACHE:
            RQ_CACHE[cpu] = []
        RQ_CACHE[cpu].append({ "time": time, "cpu": cpu, "amount": amount})

    elif line.find("EX") > -1:
        info = line.split()
        if(int(info[15]) == 231):
            cpu = int(info[16])
            pid = (int(info[17]) << 24) + (int(info[18]) << 16) + (int(info[19]) << 8) + int(info[20])
            if(pid == PID):
                if cpu in RQ_CACHE:
                    data.append(RQ_CACHE[cpu][-1]["time"])

prev = data[0]
diff_data = []
for pt in data[1:]:
    diff = pt - prev
    if diff == 0:
        continue
    diff_data.append(diff)
    prev = pt

avg = reduce(lambda x, y: x + y, diff_data) / len(diff_data)
maxa = reduce(max, diff_data)
mina = reduce(min, diff_data)


raw_data = diff_data

mu = reduce(lambda x, y: x + y, raw_data) / len(raw_data)
maxa = reduce(max, raw_data)
mina = reduce(min, raw_data)

# the histogram of the data
n, bins, patches = plt.hist(raw_data, 100, facecolor='green', alpha=0.75)

# add a 'best fit' line
plt.xlabel('Latency (ns)')
plt.ylabel('Count')
plt.title(r'$\mathrm{Histogram\ of\ RQ\ Enter\ Cycle\ period:}$')
plt.grid(True)

plt.savefig(OUTPUT + "/runqueue.png")
