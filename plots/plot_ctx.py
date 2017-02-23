import sys
import matplotlib.pyplot as plt
import Image, ImageDraw

INPUT = "input/" + sys.argv[1] + "/" + sys.argv[1] + ".prof"
PID = int(sys.argv[2])
OUTPUT = "output/" + sys.argv[1]

RQ_CACHE = dict()
data = []

prev = -1

switched_in = False

for line in open(INPUT,'r'):
    if line.find("RQ") > -1:
        info = line.split()
        time = int(info[12])
        cpu = int(info[15])
        amount = int(info[16])

        if cpu not in RQ_CACHE:
            RQ_CACHE[cpu] = []
            RQ_CACHE[cpu].append({ "time": time, "cpu": cpu, "amount": amount, "change": 0})
        else:
            if(RQ_CACHE[cpu][-1]["amount"] < amount):
                RQ_CACHE[cpu].append({ "time": time, "cpu": cpu, "amount": amount, "change": 1})
            elif(RQ_CACHE[cpu][-1]["amount"] > amount):
                RQ_CACHE[cpu].append({ "time": time, "cpu": cpu, "amount": amount, "change": -1})

    elif line.find("EX") > -1:
        info = line.split()
        if(int(info[15]) == 231):
            time = int(info[12])
            cpu = int(info[16])
            pid = (int(info[17]) << 24) + (int(info[18]) << 16) + (int(info[19]) << 8) + int(info[20])

            if(prev != time):
                if(pid == PID and switched_in == False):
                    if cpu in RQ_CACHE:
                        for r in reversed(RQ_CACHE[cpu]):
                            if(r["change"] == 1):
                                data.append({"ctx_delay": time - r["time"], "ctx_in_time": time, "RQ_CACHE": r, "cpu": cpu})
                                switched_in = True
                                break;
                elif(switched_in == True):
                    if(cpu == data[-1]["cpu"]):
                        if cpu in RQ_CACHE:
                            data[-1]["ctx_out_time"] = time
                        switched_in = False

                prev = time

# data = sorted(data, key=lambda x: x['ctx_delay'])

ctx_plain = OUTPUT + "/ctx_plain.png"
with open(ctx_plain, "wb") as out_file:
    WIDTH = 1000 + 20 # Including Margin
    SCALE = 0.1

    #Color Def
    red   = (255 , 0   , 0   )
    orange= (255 , 128 , 0   )
    green = (0   , 255 , 0   )
    blue  = (0   , 0   , 255 )
    black = (0   , 0   , 0   )
    gray  = (128 , 128 , 128 )
    white = (255 , 255 , 255 )

    size = (WIDTH, len(data) * 10 + 50)
    im = Image.new('RGB', size, white)
    draw = ImageDraw.Draw(im)

    #Sacle lines
    for i in range(WIDTH / 3, 0 + 10, -100): #Left
        draw.line([(i , 18),(i, len(data) * 10 + 30)], blue, 2)

    for i in range(WIDTH / 3, WIDTH - 10, 100): #Right
        draw.line([(i , 18),(i, len(data) * 10 + 30)], blue, 2)

    draw.text((50 - 35, 7), "1 pixel = {} us".format(SCALE), black)
    draw.text((WIDTH / 3 - 35, 7), "CTX Point", black)
    draw.line([(10, 18),(WIDTH - 10, 18)], black, 2)
    draw.line([(WIDTH / 3 , 18),(WIDTH / 3, len(data) * 10 + 30)], blue, 2)

    count = 2
    for rec in data:
        if("ctx_out_time" not in rec):
            break # missed the switched out at the end
        ctxd = rec["ctx_delay"]
        rund = rec["ctx_out_time"] - rec["ctx_in_time"]
        rq_amt = rec["RQ_CACHE"]["amount"]

        tl_pos = (WIDTH / 3 - ctxd / (SCALE * 1000), 10 * count)
        br_pos = (WIDTH / 3, 10 * count + 10)
        if(rq_amt > 1):
            draw.rectangle([tl_pos, br_pos], red)
        else:
            draw.rectangle([tl_pos, br_pos], orange)

        tl_pos = (WIDTH / 3, 10 * count + 10)
        br_pos = (WIDTH / 3 + rund / (SCALE * 1000), 10 * count)
        draw.rectangle([tl_pos, br_pos], green)

        count += 1

    del draw

    im.save(out_file, 'PNG')

raw_data = map(lambda x: x["ctx_delay"], data)

mu = reduce(lambda x, y: x + y, raw_data) / len(raw_data)
maxa = reduce(max, raw_data)
mina = reduce(min, raw_data)

# the histogram of the data
n, bins, patches = plt.hist(raw_data, 100, facecolor='green', alpha=0.75)

# add a 'best fit' line
plt.xlabel('Latency (ns)')
plt.ylabel('Count')
plt.title(r'$\mathrm{Histogram\ of\ CTX\ Delay:}$')
plt.grid(True)

plt.savefig(OUTPUT + "/ctx.png")
