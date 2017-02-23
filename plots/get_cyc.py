import sys

INPUT = "input/" + sys.argv[1] + ".cyc/" + sys.argv[1] + ".prof"

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

for pid in data:
    prev = data[pid][0]["time"]
    acc = 0
    count = -1
    mina = 0
    maxa = 1000000000000
    for pt in data[pid]:
        time = pt["time"]
        diff = time - prev

        if(diff == 0): #Handle Run away case, duplicated entry
            continue

        if(abs(diff - 1000000) > 1000000):
            break

        acc += diff
        mina = max(mina, diff)
        maxa = min(maxa, diff)

        prev = time
        count += 1

    if(count > 1000):
        if(pid > int(sys.argv[2])):
            acc = acc / count;
            print("PID: {}, mean period: {} ns, min: {}, max: {}".format(pid, acc, mina, maxa))

