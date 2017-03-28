import googlemaps
from datetime import datetime
import secret
import math

gmaps = googlemaps.Client(key=secret.KEY)

# Look up an address with reverse geocoding

def get_addr(coords):
    resp = gmaps.reverse_geocode(coords)
    addr = resp[0]['formatted_address'].split(',')[0]
    return addr

def get_times(src,dests):
    resp = gmaps.distance_matrix([src],dests,mode="walking")
    f_src = resp['rows'][0]['elements']
    res = {}
    for e,d in zip(f_src,dests):
        res[d] = int(math.ceil(e['duration']['value'] / 60.0))

    return res
    
print get_times("Burnside Hall",["Schulich Library","Redpath Library","Nahum Gelber Law Library"])
