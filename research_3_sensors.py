#!/usr/bin/python
from __future__ import print_function
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import tsl2591
import timeit
from time import sleep
import datetime as dt
import os
import serial
import time

GPIO.setmode(GPIO.BOARD)

air_quality = 40
temp_humid = 38
sound_on_off = 35
sound_data = 37
sound_clock = 36

ser = serial.Serial("/dev/ttyS0",baudrate =9600,timeout = .5)
print("  AN-137: Raspberry Pi3 to K-30 Via UART\n")
ser.flushInput()
time.sleep(1)
sum = 0

GPIO.setup(temp_humid, GPIO.IN)
path = '/home/pi/Research/Data/'
csv_data_file = path+"Data5.csv"
data_file = path+"Data5.txt"
if not os.path.exists(csv_data_file):
    with open(csv_data_file,'w') as f:
        f.write("Temp (C), Relative Humidity (%), Illumination (Lux), CO2 (ppm), Timestamp\n")
if not os.path.exists(data_file):
    with open(data_file,'w') as f:
        f.write("Data Collected every 5 minutes.\n")

while True:
    h,t = dht.read_retry(dht.DHT22, 20)
    txt = 'Temp = {0:0.1f}*C, Humidity = {1:0.1f}%, '.format(t,h)

    tsl = tsl2591.Tsl2591()  # initialize
    full, ir = tsl.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
    lux = tsl.calculate_lux(full, ir)  # convert raw values to lux
    Time = dt.datetime.today()
    #txt += "Illumination = {} lux, Timestamp = {}".format(lux, Time)
    #print(txt)
    
    
	
    
    ser.flushInput()
    ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
    time.sleep(.5)
    resp = ser.read(7)
    high = ord(resp[3])
    low = ord(resp[4])
    co2 = (high*256) + low
        
        #print "i = ",i, " CO2 = " +str(co2)
    time.sleep(.1)

    txt += "CO2 = " +str(co2)
   # print "AverageCO2 = " +str(sum/20)
    txt += ", Illumination = {} lux, Timestamp = {}\n".format(lux, Time)
    
    print(txt)
    
    with open(data_file, 'a') as f:
        f.write(txt)
    with open(csv_data_file,'a') as f:
        f.write("{},{},{},{},{}\n".format(t,h,lux,str(co2),Time))
    print("Sleeping for 5 minutes...")
    sleep(300)
