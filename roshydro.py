import requests as rq
from lxml import html
from lxml import etree
import os
import psycopg2
from datetime import datetime

conn = psycopg2.connect("dbname=reserve user=leti password=leti312 host=localhost")

def get_data(rivernum, firstday):
    fd = firstday
    print(fd)
    aname = "a-"+fd+".html"
    try:
        with open(aname, "r") as i:
            text = i.read()
    except IOError:
        print("Requesting...")
        r = rq.post("https://rushydro.ru/informer/", {"RIVER":rivernum, "DATE":firstday})
        # print(r.text)
        text = r.text
        with open(aname, "w") as o:
            o.write(text)

    root = html.fromstring(text)

    rc = root.xpath('//div[@class="ges-levels__data"]')

    return rc


#rivers = {}


def f(v):
    try:
        v = int(v)
        return v
    except ValueError:
        pass

    try:
        v = float(v)
        return v
    except ValueError:
        return None


def proc(s):
    s = s.split(",")
    s = map(f, s)
    return s


def succ(dt):
    y,m,d=dt
    if m<12:
        return [y,m+1,d]
    return [y+1,1,d]

dat = {}

def imp(rivernum, fdt, d):
    fdt=fdt[:]
    fdt.reverse()
    print(fdt)
    with open("b-{}.html".format(d), "w") as o:
        rc = get_data(1, d)
        for r in rc:
            river = r.attrib["data-river"]
            if river == "Все реки":
                continue

            # o.write("{}\n".format(river))
            for riv in r:
                reserve = riv.text
                # print(river, reserve)
                # o.write("{}\n".format(reserve))
                # dt = {}
                try:
                    for a in riv.attrib:
                        if a.startswith("water-"):
                            v = riv.attrib[a]
                            v = list(proc(v))
                            a = a.replace("water-", "").replace("-", "_")
                            # o.write("{}:{}\n".format(a, v))
                            if a=="date":
                                # print(fdt)
                                v=[datetime.strptime(str(k)+'.'+str(fdt[-1]), "%d.%m.%Y") for k in v]
                                vd = v
                            elif a=="level":
                                vl = v
                    for (d1, l1) in zip(vd, vl):
                        ll = dat.setdefault((river, reserve, d1),set())
                        ll.add(l1)
                except ValueError:
                    # print("ERROR:", a, v)
                    pass
            #rivers[river] = d
            # o.write(etree.tostring(riv, encoding=str, pretty_print=True))
        #o.write("{}".format(repr(rivers)))

rivers = {}

def st(k, v):
    (riv, res, date) = k
    print(k,v)
    quit()

def store(dat):
    cnt = 0
    for k,v in dat.items():
        if len(v)>1:
            print(k,v)

        v=list(v)[0]
        # if cnt>100:
        #     break
        cnt+=1
        st(k,v)

def impdata(rivernum):
    startdt=[2013, 6, 1] # "01-06-2013"
    enddt  =[2023,12,12] # "12-12-2023"
    dt = startdt
    while dt <= enddt:
        d = "{2}-{1}-{0}".format(*dt)
        print(d, dt)
        imp(rivernum, dt, d)
        dt=succ(dt)

def main():
    # fdt = "01.01.2020"
    global dat
    impdata(1)
    # dat=list(dat)
    # dat.sort()
    store(dat)
    quit()
    # fdt = os.environ.get("Y","01-01-2023")


if __name__ == '__main__':
    main()
