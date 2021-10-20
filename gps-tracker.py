#!/usr/bin/env python3

import datetime
import serial
from datetime import timezone


port = "/dev/ttyACM0"


def parse_gps(data):
    data = data.decode('UTF-8')
    # print("raw:", data) #prints raw data
    if data[0:6] == '$GPRMC':

        split_data = data.split(",")
        # print("data: ", split_data)
            
        hour = int(split_data[1][0:2])
        minute = int(split_data[1][2:4])
        second = int(split_data[1][4:6])
        time = str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
            
        month = int(split_data[9][2:4])
        day = int(split_data[9][0:2])
        year = 2000 + int(split_data[9][4:6])
        date = str(year).zfill(4) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)
            
        date_time = date + " " + time
        epoch = get_epoch(year, month, day, hour, minute, second)
            
        lat = split_data[3]
        dir_lat = split_data[4]
        lng = split_data[5]
        dir_lng = split_data[6]

        if lat != '' and lng != '':
            lat_dd = decimal_degrees(*dm(float(lat)))
            lng_dd = decimal_degrees(*dm(float(lng)))
           
            lat_dd = lat_dd if dir_lat == 'N' else -lat_dd
            lng_dd = lng_dd if dir_lng == 'E' else -lng_dd
            
            speed = float(split_data[7]) * 1.15078
          
            print("%s, %s, Lat: %s, Lng: %s, Speed: %s" % (
                date_time, epoch, format(lat_dd, '.6f'), format(lng_dd, '.6f'), format(speed, '.2f')))
          
            f = open("log_" + str(year) + str(month) + str(day) + ".txt", "a")
            f.write(str(date_time) + ", "
                + str(epoch) + ", "
                + format(lat_dd, '.6f') + ", "
                + format(lng_dd, '.6f') + ", "
                + format(speed, '.2f') + "\n")
            f.close()
        else:
            print("No GPRMC Data:")
            print(split_data)

    # if data[0:6] == '$GPGGA':
    #    split_data = data.split(",")
    #    alt_m = float(split_data[9])
    #    alt_f = alt_m * 3.28084
    #    print("Alt(m): %s, Alt(f): %s" % (format(alt_m, '.2f'), format(alt_f, '.2f')))


def get_epoch(year, month, day, hour, minute, second):
    # Converts Date and Time to Epoch Timestamp
    native = datetime.datetime(year, month, day, hour, minute, second)
    aware = native.replace(tzinfo=timezone.utc).timestamp()
    return round(aware)


def dm(x):
    degrees = int(x) // 100
    minutes = x - 100 * degrees
    return degrees, minutes


def decimal_degrees(degrees, minutes):
    return degrees + minutes / 60


print("Receiving GPS data")

ser = serial.Serial(port, baudrate=9600, timeout=0.5)
while True:
    raw_data = ser.readline()
    parse_gps(raw_data)
