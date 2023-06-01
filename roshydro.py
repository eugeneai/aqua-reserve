import requests as rq
from lxml import html
from lxml import etree


def get_data(rivernum, firstday):
    # r = rq.post("https://rushydro.ru/informer/", {"RIVER":rivernum, "DATE":firstday})
    # print(r.text)
    #text = r.text
    with open("./a.html") as i:
        text = i.read()
    root = html.fromstring(text)

    #rc = root.xpath("//div/@ges-levels__data/../option")
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


def main():
    with open("./b.html", "w") as o:
        rc = get_data(1, "01-01-2017")
        for r in rc:
            river = r.attrib["data-river"]
            o.write("{}\n".format(river))
            d = {}
            for riv in r:
                reserve = riv.text
                o.write("{}\n".format(reserve))
                dt = {}
                for a in riv.attrib:
                    if a.startswith("water-"):
                        v = riv.attrib[a]
                        v = list(proc(v))
                        a = a.replace("water-", "").replace("-", "_")
                        o.write("{}:{}\n".format(a, v))
                        dt[a] = v
                d[reserve] = dt
            rivers[river] = d
            # o.write(etree.tostring(riv, encoding=str, pretty_print=True))
        o.write("\n-------------\n")
        o.write("{}".format(rivers))


if __name__ == '__main__':
    main()
