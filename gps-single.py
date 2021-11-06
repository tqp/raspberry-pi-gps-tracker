#!/usr/bin/env python3

import time
import datetime
import serial
from datetime import timezone

port = "/dev/ttyACM0"
fix = False

# GPGGA
gpgga_split_data = ""
gpgga_data_received = False
gpgga_time_utc = ""
gpgga_lat = ""
gpgga_lat_dir = ""
gpgga_lng = ""
gpgga_lng_dir = ""
gpgga_quality = ""
gpgga_num_satellite = ""
gpgga_altitude = ""
gpgga_altitude_unit = ""

# GPVTG
gpvtg_split_data = ""
gpvtg_data_received = False
gpvtg_speed_in_knots = ""
gpvtg_speed_in_kph = ""
gpvtg_speed_in_mph = ""

# GPRMC
gprmc_split_data = ""
gprmc_data_received = False
gprmc_time_utc = ""
gprmc_date = ""
gprmc_pos_status = ""
gprmc_lat = ""
gprmc_lat_dir = ""
gprmc_lng = ""
gprmc_lng_dir = ""
gprmc_speed_in_knots = ""
gprmc_date = ""
gprmc_data_received = False

gprmc_hour = ""
gprmc_minute = ""
gprmc_second = ""
gprmc_time = ""
gprmc_month = ""
gprmc_day = ""
gprmc_year = ""
gprmc_date = ""
grpmc_date_time = ""
gprmc_epoch = ""


def parse_gps(data):
    global fix
    global gpgga_split_data, gpgga_data_received
    global gpgga_quality, gpgga_num_satellite
    data = data.decode('UTF-8')
    #print("------------")
    #print("Data Stream: " + data)


    # GPGGA: Determine GPS fix with GPGGA data.
    if (not fix) & (len(data) > 0) & (data[0:6] == '$GPGGA'):
        #print("GPGGA: Checking GPGGA data: %s" % (data))
        gpgga_split_data = data.split(",")
        gpgga_quality = gpgga_split_data[6]
        gpgga_num_satellite = gpgga_split_data[7]
        if gpgga_quality.isdigit() & int(gpgga_quality) > 0:
            print("Found Fix!")
            fix = True
        else:
            print("Waiting for Fix... Signal: " + gpgga_quality + ", Satellites: " + gpgga_num_satellite)
            fix = False
    else:
        time.sleep(0)
        
    # GPGGA: If we have a good fix, also get GPGGA (position) data.
    if fix & ((len(data) > 0) & (data[0:6] == '$GPGGA')):
        print("GPGGA: Receiving GPGGA data: %s" % (data))
        global gpgga_time_utc, gpgga_lat, gpgga_lat_dir, gpgga_lng, gpgga_lng_dir, gpgga_altitude, gpgga_altitude_unit
        gpgga_split_data = data.split(",")
        gpgga_time_utc = gpgga_split_data[1]
        gpgga_lat = gpgga_split_data[2]
        gpgga_lat_dir = gpgga_split_data[3]
        gpgga_lng = gpgga_split_data[4]
        gpgga_lng_dir = gpgga_split_data[5]
        gpgga_quality = gpgga_split_data[6]
        gpgga_num_satellite = gpgga_split_data[7]
        gpgga_altitude = gpgga_split_data[8]
        gpgga_altitude_unit = gpgga_split_data[10]
        gpgga_data_received = True

    # GPVTG: If we have a good fix, also get GPVTG (speed) data.
    if fix & ((len(data) > 0) & (data[0:6] == '$GPVTG')):
        print("GGVTG: Receiving GPVTG data: %s" % (data))
        global gpvtg_speed_in_knots, gpvtg_speed_in_kph
        global gpvtg_split_data, gpvtg_data_received
        gpvtg_split_data = data.split(",")
        #print("%s" % (str(gpvtg_data)))
        gpvtg_speed_in_knots = gpvtg_split_data[5]
        gpvtg_speed_in_kph = gpvtg_split_data[7]
        gpvtg_data_received = True
        #print("Speed: %s/%s" % (speed_in_knots, speed_in_kph))
    
    # GPRMC: If we have a good fix, also get GPRMC (GPS-specific) data.
    if fix & ((len(data) > 0) & (data[0:6] == '$GPRMC')):
        print("GPRMC: Receiving GPRMC data: %s" % (data))
        global gprmc_split_data, gprmc_data_received
        global gprmc_time_utc, gprmc_hour, gprmc_minute, gprmc_second, gprmc_time
        global gprmc_month, gprmc_day, gprmc_year, gprmc_date, gprmc_date_time, gprmc_epoch
        global gprmc_pos_status, gprmc_lat, gprmc_lat_dir, gprmc_lng, gprmc_lng_dir, gprmc_speed_in_knots, gprmc_date
        gprmc_split_data = data.split(",")
        gprmc_time_utc = gprmc_split_data[1]
        gprmc_pos_status = gprmc_split_data[2]
        gprmc_lat = gprmc_split_data[3]
        gprmc_lat_dir = gprmc_split_data[4]
        gprmc_lng = gprmc_split_data[5]
        gprmc_lng_dir = gprmc_split_data[6]
        gprmc_speed_in_knots = gprmc_split_data[7]
        gprmc_date = gprmc_split_data[9]
        gprmc_data_received = True

        gprmc_hour = int(gprmc_time_utc[0:2])
        gprmc_minute = int(gprmc_time_utc[2:4])
        gprmc_second = int(gprmc_time_utc[4:6])
        gprmc_time = str(gprmc_hour).zfill(2) + ":" + str(gprmc_minute).zfill(2) + ":" + str(gprmc_second).zfill(2)

        gprmc_month = int(gprmc_date[2:4])
        gprmc_day = int(gprmc_date[0:2])
        gprmc_year = 2000 + int(gprmc_date[4:6])
        gprmc_date = str(gprmc_year).zfill(4) + "-" + str(gprmc_month).zfill(2) + "-" + str(gprmc_day).zfill(2)

        gprmc_date_time = gprmc_date + " " + gprmc_time
        gprmc_epoch = get_epoch(gprmc_year, gprmc_month, gprmc_day, gprmc_hour, gprmc_minute, gprmc_second)

    # Output    
    if gpgga_data_received:
        lat_dd = get_dd(gpgga_lat)
        lng_dd = get_dd(gpgga_lng)
            
        print("--------------------------")
        print("GPGGA:        : %s" % (gpgga_split_data))
        print("time_utc      : %s" % (gpgga_time_utc))
        #print("epoch         : %s" % (get_epoch_from_utc(gpgga_time_utc)))
        print("lat           : %s" % (gpgga_lat))
        print("lat_dir       : %s" % (gpgga_lat_dir))
        print("lat_dd        : %s" % (lat_dd))
        print("lng           : %s" % (gpgga_lng))
        print("lng_dir       : %s" % (lng_dd))
        print("lng           : %s" % (gpgga_lng))
        print("quality       : %s" % (gpgga_quality))
        print("num_satellite : %s" % (gpgga_num_satellite))
        print("altitude      : %s" % (gpgga_altitude))
        print("altitude_unit : %s" % (gpgga_altitude_unit))
       
    if gpvtg_data_received: 
        print("--------------------------")
        print("GPVTG:        : %s" % (gpvtg_split_data))
        if len(gpvtg_speed_in_knots) > 0:
            print("speed_in_knots: %s" % (gpvtg_speed_in_knots))
        if len(gpvtg_speed_in_kph) > 0:
            print("speed_in_kph  : %s" % (gpvtg_speed_in_kph))
            gpvtg_speed_in_mph = float(str(gpvtg_speed_in_kph)) * 1.15078
            print("speed_in_mph  : %s" % (gpvtg_speed_in_mph))

    if gprmc_data_received:
        lat_dd = get_dd(gprmc_lat)
        lng_dd = get_dd(gprmc_lng)
        print("--------------------------")
        print("GPRMC:        : %s" % (gprmc_split_data))
        print("time_utc      : %s" % (gprmc_time_utc))
        print("date          : %s" % (gprmc_date))
        print("lat           : %s" % (gprmc_lat))
        print("lat_dir       : %s" % (gprmc_lat_dir))
        print("lat_dd        : %s" % (lat_dd))
        print("lng           : %s" % (gprmc_lng))
        print("lng_dir       : %s" % (gprmc_lng_dir))
        print("lng_dd        : %s" % (lng_dd))
        print("lng           : %s" % (gprmc_lng))
        print("date_time     : %s" % (gprmc_date_time))
        print("epoch         : %s" % (gprmc_epoch))

    if gpgga_data_received & gpvtg_data_received & gprmc_data_received:
        print("Got everything. Writing to file...")
        str_to_write = str(gprmc_date_time) + ", " + str(gprmc_epoch) + ", " + format(lat_dd, '.6f') + ", " + format(lng_dd, '.6f') + ", " + format(gpvtg_speed_in_mph, '.2f') + ", " + format(float(gpgga_altitude), '.2f') + "\n"
        print(str_to_write)
        write_to_file(str_to_write)
        #exit()
        time.sleep(1)

def write_to_file(string):
    f = open("log_" + str(gprmc_year) + str(gprmc_month) + str(gprmc_day) + ".txt", "a")
    f.write(string)
    f.close()

def get_dd(l):
    return decimal_degrees(*dm(float(l)))

def get_epoch_from_utc(utc):
    hour = int(utc[0:2])
    minute = int(utc[2:4])
    second = int(utc[4:6])
    time = str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
    
    month = int(utc[2:4])
    day = int(utc[0:2])
    year = 2000 + int(utc[4:6])
    date = str(year).zfill(4) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)

    date_time = date + " " + time

    # Converts Date and Time to Epoch Timestamp
    print("Year: " + str(year) + ", Month: " + str(month) + ", Day: " + str(day) + ", Hour: " + str(hour) + ", Minute: " + str(minute) + ", Second: " + str(second))
    native = datetime.datetime(year, month, day, hour, minute, second)
    aware = native.replace(tzinfo=timezone.utc).timestamp()
    return round(aware)

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

gpsConnection = False
while not gpsConnection:
    try:
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        gpsConnection = True
    except Exception as e:
        print("Could not access GPS. Trying again in 10 seconds..." + str(e))
        time.sleep(10)

while True:
    raw_data = ser.readline()
    parse_gps(raw_data)
