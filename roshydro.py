import requests as rq
from lxml import html
from lxml import etree
import os

def get_data(rivernum, firstday):
    fd = firstday.replace(".","-")
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


rivers = {}


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

def impdata(rivernum):
    startdt=[2017,1,1] # "01-01-2017"
    enddt=[2023,12,12] # "12-12-2023"
    dt = startdt
    while dt <= enddt:
        d = "{2}-{1}-{0}".format(*dt)
        print(dt)
        dt=succ(dt)

def main():
    # fdt = "01.01.2020"
    impdata(1)
    quit()
    fdt = os.environ.get("Y","01-01-2023")
    with open("b-{}.html".format(fdt.replace(".","-")), "w") as o:
        rc = get_data(1, fdt)
        for r in rc:
            river = r.attrib["data-river"]
            # o.write("{}\n".format(river))
            d = {}
            for riv in r:
                reserve = riv.text
                # o.write("{}\n".format(reserve))
                dt = {}
                for a in riv.attrib:
                    if a.startswith("water-"):
                        v = riv.attrib[a]
                        v = list(proc(v))
                        a = a.replace("water-", "").replace("-", "_")
                        # o.write("{}:{}\n".format(a, v))
                        dt[a] = v
                d[reserve] = dt
            rivers[river] = d
            # o.write(etree.tostring(riv, encoding=str, pretty_print=True))
        o.write("{}".format(repr(rivers)))


if __name__ == '__main__':
    main()
