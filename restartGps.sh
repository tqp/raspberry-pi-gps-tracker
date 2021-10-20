#!/bin/bash

sudo service gpsd stop
sudo gpsd -nN /dev/ttyACM0 /var/run/gpsd.sock
