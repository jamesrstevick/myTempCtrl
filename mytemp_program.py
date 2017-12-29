# Copyright 2013-2017 Clarity Movement Co.

# Benchmark myTemp Temperature Chamber
# Clarity Movement Co.
# James Stevick

###########################################
# Program for controlling myTemp
###########################################

import time
import serial
import struct

import lib_mytemp

# Find COM port
port = lib_mytemp.port_finder()
if port == []:
    print("No COM port found, QUIT")
    quit()

# Make serial connection to Arduino
connected, myT = lib_mytemp.mytemp_connect(port)
if connected == False:
    print("Failed to connect to {}".format(port))
    quit()

time.sleep(2) # Necessary delay for Arduino Uno
print("Running myTemp program")


###############################
###   WRITE PROGRAM BELOW   ###
###############################

# # Examples provided

# Sets temperature to input
myT.set_temp(25.7)

# Sets time to input
myT.set_time(572)

# Increase temperature by 5.3 C
myT.change_settings(1, 1, 5.3)
# Decrease time by 10 minutes
myT.change_settings(0, 0, 10)
