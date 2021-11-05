#!/usr/bin/env python3

import time

import serial

port = "/dev/ttyACM0"
fix = False

received_gpgga_data = False
received_gpvtg_data = False
utc = ""
lat = ""
lat_dir = ""
lng = ""
lng_dir = ""
quality = ""
num_satellite = ""
altitude = ""
altitude_unit = ""
speed_in_knots = ""
speed_in_kph = ""


def parse_gps(data):
    data = data.decode('UTF-8')
    updated_gpgga = False
    # print("raw:", data)

    # Check Fix
    if (len(data) > 0) & (data[0:6] == '$GPGGA'):
        split_data = data.split(",")
        status = split_data[6]
        if status.isdigit() & int(status) > 0:
            global fix
            fix = True
        else:
            fix = False

        if fix:
            # print("Fix: %s %s" % (fix, str(split_data)))
            global utc, lat, lat_dir, lng, lng_dir, quality, num_satellite, altitude, altitude_unit
            global received_gpgga_data
            utc = split_data[1]
            lat = split_data[2]
            lat_dir = split_data[3]
            lng = split_data[4]
            lng_dir = split_data[5]
            quality = split_data[6]
            num_satellite = split_data[7]
            altitude = split_data[8]
            altitude_unit = split_data[10]
            received_gpgga_data = True

    if fix:
        if (len(data) > 0) & (data[0:6] == '$GPVTG'):
            # print("Receiving GPVTG Data...")
            global speed_in_knots, speed_in_kph
            global received_gpvtg_data
            gpvtg_data = data.split(",")
            # print("%s" % (str(gpvtg_data)))
            speed_in_knots = gpvtg_data[5]
            speed_in_kph = gpvtg_data[7]
            received_gpvtg_data = True
            # print("Speed: %s/%s" % (speed_in_knots, speed_in_kph))
    else:
        print("Waiting for Fix...")
        time.sleep(1)

    if received_gpgga_data & received_gpvtg_data:
        print("--------------------------")
        print("utc           : %s" % (utc))
        print("lat           : %s" % (lat))
        print("lat_dir       : %s" % (lat_dir))
        print("lng           : %s" % (lng))
        print("lng_dir       : %s" % (lng_dir))
        print("quality       : %s" % (quality))
        print("num_satellite : %s" % (num_satellite))
        print("altitude      : %s" % (altitude))
        print("altitude_unit : %s" % (altitude_unit))
        print("speed_in_knots: %s" % (speed_in_knots))
        print("speed_in_kph  : %s" % (speed_in_kph))
        print("--------------------------")
        updated_gpgga = False
        exit()
        time.sleep(1)


print("Receiving GPS data")

gpsConnection = False
while not gpsConnection:
    try:
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        gpsConnection = True
    except Exception as e:
        print("Could not access GPS. Trying again in 5 seconds..." + str(e))
        time.sleep(5)

while True:
    raw_data = ser.readline()
    parse_gps(raw_data)
