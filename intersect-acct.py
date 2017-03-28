#!/usr/bin/env python

from collections import namedtuple
import time
import sys
import math

GRACE_TIME = 30
GRACE_PCT = 0.3
GRACE_MIN = 5

Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

seats = {}
import sqlite3
conn = sqlite3.connect('/Users/npaunl/libseat.db')
c = conn.cursor()

def load_seats(area):
  res = c.execute("SELECT seat, xmin, ymin, xmax, ymax FROM seating WHERE area = ?", (area,))
  for sid,xmin,ymin,xmax,ymax in res:
      seats[sid] = Rectangle(xmin,ymin,xmax,ymax)

  print len(seats), "seats loaded"
      
def renew(seat):
    curr = c.execute("SELECT entry, renew FROM occupancy WHERE seat = ?",(seat,)
    )
    t = int(time.time())
    n_entry = t
    for entry, renew in curr:
        if entry != 0:
            n_entry = entry

    
    n_renew = t
    print "\033[1;34mSeat %s OCCUPIED\033[0m" % seat
    print "\007"
    c.execute("UPDATE occupancy SET entry = ?, renew = ? WHERE seat = ?",(n_entry,n_renew,seat))
    conn.commit()


def prune(seat):
    curr = c.execute("SELECT entry, renew FROM occupancy WHERE seat = ?", (seat,))
    for entry, renew in curr:
        t = int(time.time())
        if entry != 0:
            since_renew = t - renew
            tenure = renew - entry

            if (since_renew >= max(min(GRACE_TIME,GRACE_PCT * tenure),GRACE_MIN)):
                print "\007"
                c.execute("UPDATE occupancy SET entry = 0, renew = 0 WHERE seat = ?", (seat,))
                print "\033[1;34mSeat %s VACATED\033[0m" % seat
                conn.commit()




def produce_res(res):
    for seat in sorted(seats.keys()):
        if seat in res:
            if 'heuristic' in res[seat]:
                renew(seat)
            else:
                print seat, res[seat]['state']
        else:
            prune(seat)

def load_cv(f):
    res = {}
    rev = {}
    while True:
        a = f.readline()[:-1].split(" ")
        if a[0] == '*':
            produce_res(res)
            res = {}
            rev = {}
            continue

        xmin,ymin,xmax,ymax = [int(x) for x in a[1:5]]
        cf = float(a[5])
        rect = Rectangle(xmin,ymin,xmax,ymax)
        for sid,srect in seats.items():
            h =  cf*(float(area(rect,srect))/float(area(srect,srect))) # CV0 198 0 379 245 0.880198
            if h > 0.5:

                if sid in res:
                    res[sid]['state'] = '> 1 persons to a seat'
                    #res[sid]['match'].append(rect)
                    if 'heuristic' in res[sid]:
                        del res[sid]['heuristic']

                if rect in rev:
                    res[rev[rect]]['state'] = '> 1 seats for one person'

                    if 'heuristic' in res[rev[rect]]:
                        del res[rev[rect]]['heuristic']
                    res[sid] = {'match': rect, 'state': '> 1 seats for one person'}
                else:
                    res[sid] = {'match': rect, 'heuristic': h, 'state': '1:1 correspondance'}
                    rev[rect] = sid
  

# intersection here is (3, 3, 4, 3.5), or an area of 1*.5=.5

def area(a, b):  # returns None if rectangles don't intersect
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if (dx>=0) and (dy>=0):
        return dx*dy
    else:
        return 0

load_seats(sys.argv[1])
load_cv(sys.stdin)
