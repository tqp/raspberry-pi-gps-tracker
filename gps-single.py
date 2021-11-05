#!/usr/bin/env python3

import datetime
import serial
import time

from datetime import timezone

port = "/dev/ttyACM0"

def parse_gps(fix, data):
    data = data.decode('UTF-8')
    print("raw:", data)

    # Check Fix
    if ((len(data) > 0) & (data[0:6] == '$GPGGA')):
        split_data = data.split(",")
        status = split_data[6]
        if(status.isdigit()):
            fix = int(status) > 0
            print("Fix: %s %s" % (fix, str(split_data)))
            time=split_data[2]
            lat=split_data[3]
            lat_dir=split_data[4]
            lng=split_data[5]
            lng_dir=split_data[6]
            quality=split_data[7]
            num_satellite=data[8]
            altitude=split_data[10]
            altitude_unit=split_data[11]
    
    if (fix):
        print("Continuing...")
        #if ((len(data) > 0) & (data[0:6] == '$GPVTG')):
        #    print("Receiving GPVTG Data...")
        #    split_data = data.split(",")
        #    print("Type: %s" % (split_data[1]))
    else:
        print("Waiting for Fix...")
        time.sleep(1)


print("Receiving GPS data")

fix = False
lat = 0
lng = 0

gpsConnection = False
while gpsConnection != True:
    try:
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        gpsConnection = True
    except:
        print("Could not access GPS. Trying again in 5 seconds...")
        time.sleep(5)

while True:
    raw_data = ser.readline()
    parse_gps(fix, raw_data)
