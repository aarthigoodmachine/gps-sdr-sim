import csv
import requests

"""
A small script to increase the altitude and spit out a CSV that we can feed into gps-sdr-sim
"""
# Reykjavík, Iceland :) 
LAT = 64.128288
LON = -21.827774

ALT_OF_INTEREST = 20000 # meters. 20 km is when most IMU chips will cut out
MAX_ALT = 30000 # meters
ALT_DELTA = 10 # meters
STARTING_ALT = 0 # meters
COUNTER_DELT = 0.1

def up(alt, meters):
    return alt + meters

def down(alt, meters):
    return alt - meters

def main():
    coords = list()
    counter = 0.0
    alt = STARTING_ALT
    while (alt < MAX_ALT):
        alt = up(alt, ALT_DELTA)
        counter += COUNTER_DELT
        coords.append((counter,LAT,LON, alt))
    while (alt > STARTING_ALT):
        alt = down(alt, ALT_DELTA)
        counter += COUNTER_DELT
        coords.append((counter,LAT,LON,alt))
    with open("out.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(coords)
    

    if __name__ == "__main__":
        main()

    
