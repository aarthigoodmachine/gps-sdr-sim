# Description
Will spit out a .csv with lat,lon,alt to feed into `gps-sdr-sim`

# How to use 
Get output csv file (should already be in `altutude_changer/src/out.csv`):
`python altitude_changer.py`

Run that through gps-sdr-sim to get the simulation data:
` ./gps-sdr-sim -b 8 -e <the latest ephemeral file (like brdc0010.23.n)> -x ../../goodmachine/balloon/lora_GPS_tracker_ESP32/packages/gps-sdr-sim/altitude_changer/src/out.csv`

Transmit over hackrf:
`hackrf_transfer -t gpssim.bin -f 1575420000 -s 2600000 -a 1 -x 0`

Observe results over serial port)