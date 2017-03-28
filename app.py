#!/usr/bin/env python
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
import gmape

import sqlite3
import json
conn = sqlite3.connect('/Users/npaunl/libseat.db')
c = conn.cursor()

def get_total_seats(lid):
     res = c.execute("SELECT COUNT(*) as ct  FROM occupancy JOIN seating on seating.seat = occupancy.seat JOIN areas ON areas.area = seating.area WHERE library = ?",(lid,))
     for ct, in res:
        return int(ct)

def get_filled_seats(lid):
    res = c.execute("SELECT COUNT(*) as ct  FROM occupancy JOIN seating on seating.seat = occupancy.seat JOIN areas ON areas.area = seating.area WHERE library = ? AND entry <> 0",(lid,))
    for ct, in res:
        return int(ct)



def libraries(form):
    loc = form['loc'].value
    addr = gmape.get_addr(loc)
    res = c.execute("SELECT * FROM libraries")
    libs = {}
    ads = {}
    lids = {}
    for lid,name, laddr in res:
        libs[name] = laddr
        ads[laddr] = name
        lids[name] = lid

    times = gmape.get_times(addr,libs.values())
    lib_struct = []
    for k,v in times.items():
        used = get_filled_seats(lids[ads[k]])
        total = get_total_seats(lids[ads[k]])
        free = total - used
        if total > 0:
            availability  = float(free)/float(total) * 100
        else:
            availability = "NaN"
        struct = {'name': ads[k], 'dist': v,'free': free, 'availability': availability}
        lib_struct.append(struct)

    print "Content-Type: text/json"
    print ""
    print json.dumps(lib_struct)


if 'query' not in form:
    print "Content-Type: text/html"
    print ""
    print "Error"
    raise SystemExit
else:
    qv = form['query'].value
    if qv == 'libraries':
        libraries(form)
    elif qv == 'floors':
        floors(form)
    elif qv == 'floor':
        floor(form)
