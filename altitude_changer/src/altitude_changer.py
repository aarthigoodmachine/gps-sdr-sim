import csv
import math
import numpy as np # this is unbelievably annoying for just needing a range of values w/ a delta of 0.1, but because of floating point arithemtic in python, i guess this is necessary....
import requests

"""
A small script to increase the altitude and spit out a CSV that we can feed into gps-sdr-sim
"""

LENGTH_OF_TEST = 3 # in hours
HZ = 10 
# TOTAL SAMPLES TO RUN FOR 3 HOURS
NUM_SAMPLES = 3600 * HZ * LENGTH_OF_TEST
# LAUNCH SITE 
LAT = 25.5
LON = -145.1
# HORIZONTAL SPEED
SPEED = 4 # M/S
KM_PER_DEGREE = 111.32 # 1 decimal degree/111.32 km

ALT_OF_INTEREST = 20000 # meters. 20 km is when most IMU chips will cut out
MAX_ALT = 30000 # meters
ALT_DELTA = 10 # meters
STARTING_ALT = 0 # meters
COUNTER_DELT = 0.1


def meters_to_decimal_degrees(meter, latitude):
    return meter/((KM_PER_DEGREE*1000*math.cos(latitude*(math.pi/180))))

def up(alt, meters):
    return alt + meters

def down(alt, meters):
    return alt - meters

def main():
    alts = list()
    longs = list()
    alt = STARTING_ALT
    lon = LON
    while(len(alts)<NUM_SAMPLES):
        while (alt < MAX_ALT):
            alt = up(alt, ALT_DELTA)
            alts.append(alt)
            lon += (meters_to_decimal_degrees(SPEED,LAT))
            longs.append(lon)
        while (alt > STARTING_ALT):
            alt = down(alt, ALT_DELTA)
            alts.append(alt)
            lon -= (meters_to_decimal_degrees(SPEED,LAT))
            longs.append(lon)
    counters = np.arange(0, 0 + len(alts) * 0.1, 0.1).tolist()
    counters = np.round(counters,1)
    with open("out.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(list(zip(counters,[LAT]*len(alts), longs, alts)))

if __name__ == "__main__":
    main()

    
