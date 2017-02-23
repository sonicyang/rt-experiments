import sys
import matplotlib.pyplot as plt


INPUT = "input/" + sys.argv[1] + "/" + sys.argv[1] + ".prof"
PID = int(sys.argv[2])
OUTPUT = "output/" + sys.argv[1]

data = dict()
for line in open(INPUT,'r'):
    if line.find("EX") > -1:
        info = line.split()
        if(int(info[15]) == 231):
            time = int(info[12])
            cpu = int(info[16])
            pid = (int(info[17]) << 24) + (int(info[18]) << 16) + (int(info[19]) << 8) + int(info[20])
            if pid not in data:
                data[pid] = []
            data[pid].append({ "time": time, "cpu": cpu })

prev = data[PID][0]["time"]
diff_data = []
for pt in data[PID][1:]:
    diff = pt["time"] - prev
    if diff == 0:
        continue
    diff_data.append(diff)
    prev = pt["time"]

raw_data = diff_data

mu = reduce(lambda x, y: x + y, raw_data) / len(raw_data)
maxa = reduce(max, raw_data)
mina = reduce(min, raw_data)

# the histogram of the data
n, bins, patches = plt.hist(raw_data, 100, facecolor='green', alpha=0.75)

# add a 'best fit' line
plt.xlabel('Latency (ns)')
plt.ylabel('Count')
plt.title(r'$\mathrm{Histogram\ of\ CTX\ Cycle\ period:}$')
plt.grid(True)

plt.savefig(OUTPUT + "/cyc.png")
