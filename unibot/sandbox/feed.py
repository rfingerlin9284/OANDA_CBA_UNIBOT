import csv, random
def load_csv(path):
    with open(path,"r",newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            yield {"ts":row.get("ts"),
                   "o":float(row["open"]),"h":float(row["high"]),
                   "l":float(row["low"]),"c":float(row["close"])}
def synthetic(n=2000,start=1.10000,vol=0.0005):
    price=start
    for i in range(n):
        ret=random.gauss(0.0,vol)
        o=price; c=o*(1.0+ret)
        hi=max(o,c)*(1.0+abs(random.gauss(0,vol/2)))
        lo=min(o,c)*(1.0-abs(random.gauss(0,vol/2)))
        price=c
        yield {"ts":str(i),"o":o,"h":hi,"l":lo,"c":c}
