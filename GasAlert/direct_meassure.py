__author__ = 'ClassicMike'
import urllib2
import urllib
import RPi.GPIO as GPIO
import subprocess
import socket
from hx711 import HX711
import sys

#setup GPIO using Board numbering
#GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)


#BT read
#!/usr/bin/env python
import time
import serial
import os.path



#create sensors
hx1 = HX711(5, 6)
hx1.set_reading_format("LSB", "MSB")
hx1.set_reference_unit(92)
hx1.reset()
hx1.tare()

hx1 = HX711(13, 19)
hx1.set_reading_format("LSB", "MSB")
hx1.set_reference_unit(92)
hx1.reset()
hx1.tare()

def getmedida():
    val = hx.get_weight(5)
    print val
    hx.power_down()
    hx.power_up()

    time.sleep(0.5)
    return val


while 1:
    hx1.set_gain(128)
    print hx1.read()
    time.sleep(1)
    hx1.set_gain(32)
    print hx1.read()
    time.sleep(1)
