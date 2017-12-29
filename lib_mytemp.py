# Copyright 2013-2017 Clarity Movement Co.

# Benchmark myTemp Temperature Chamber
# Clarity Movement Co.
# James Stevick

###########################################
# Library for controlling myTemp
###########################################

import os
import sys
import time
import serial
import struct

# Connects to myTemp COM port
def port_finder():
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]
    else:
        raise EnvironmentError('unsupported platform.')
    list_of_ports = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            list_of_ports.append(port)
            print('Found port ({}).'.format(port))
        except (OSError, serial.SerialException):
            pass
    return list_of_ports


# Connect to myTemp, returns boolean and serial connection
def mytemp_connect(list_of_ports):

    print('Connecting to myTemp')
    connected = False

    for port in list_of_ports:
        try:
            myT = MyTempControl(port)
            connected = True
        except:
            myT.close()
            print('Failed to connect to {}.'.format(port))
            pass

    return connected, myT

class MyTempControl():
    GET_ID = b'\x53\x54'
    SET = b'\x53\x45'
    SHIFT =  b'\x53\x48'
    DECREASE =  b'\x53\x44'
    INCREASE =  b'\x53\x49'
    ID = b'\x4D\x59\x54'

    def __init__(self, com, baudrate=9600):
        self._com_port = com
        self._baudrate = baudrate
        self._ser = None
        try:
            self._ser = serial.Serial(
                self._com_port, self._baudrate, timeout=3)
        except:
            print('Serial Connection could not be established for: ' +
                  com + ' at ' + str(baudrate))


    # Check ID of myTemp, returns boolean
    def is_mytemp(self):
        self._ser.flush()
        self._ser.write(self.GET_ID)
        t0 = time.time()
        while self._ser.in_waiting < 3:
            if time.time() - t0 > 3:
                self._ser.flush()
                return False
        readID = self._ser.read(3)
        if readID == self.ID:
            self._ser.flush()
            return True
        else:
            self._ser.flush()
            return False


    # Press Set and number of presses
    def press_set(self,num=1):
        for i in range(num):
            self._ser.flush()
            self._ser.write(self.SET)
            time.sleep(0.5)


    # Press Shift and number of presses
    def press_shift(self,num=1):
        for i in range(num):
            self._ser.flush()
            self._ser.write(self.SHIFT)
            time.sleep(0.5)

    # Press Decrease and number of presses
    def press_dec(self,num=1):
        for i in range(num):
            self._ser.flush()
            self._ser.write(self.DECREASE)
            time.sleep(0.5)


    # # Press Increase and number of presses
    def press_inc(self,num=1):
        for i in range(num):
            self._ser.flush()
            self._ser.write(self.INCREASE)
            time.sleep(0.5)


    # Resets temperature to 0.0 C
    def reset_temp(self):
        time.sleep(2)
        print('Setting temperature to 0.0 C')
        self.press_set()
        self.press_shift(3)
        self.press_dec()
        self.press_set(2)


    # Reset Time to 0 minutes
    def reset_time(self):
        time.sleep(2)
        print('Setting time to 0 minutes')
        self.press_set(2)
        self.press_shift(3)
        self.press_dec(10)
        self.press_set()
    

    # Set absolute temperature: between 0.0 and 60.0 C
    def set_temp(self,temp):

        # Set temperature to 0.0 C
        self.reset_temp()

        print('Setting temperature to {} C'.format(temp))

        # Ensure value to 1 decimal between 0.0 and 60.0 C
        temp = int(temp*10+0.5)
        if temp > 600:
            print('Temperature out of range, set to 60 C')
            temp = 600

        # Determine increase to each figure
        tens = divmod(temp,100)[0]
        temp = divmod(temp,100)[1]
        dig = divmod(temp,10)[0]
        dec = divmod(temp,10)[1]

        # Set temperature
        self.press_set()
        self.press_inc(dec)
        self.press_shift()
        self.press_inc(dig)
        self.press_shift()
        self.press_inc(tens)
        self.press_set(2)


    # Set absolute time: between 0 and 9999 min
    def set_time(self,time):

        # Set time to 0
        self.reset_time()

        print('Setting time to {} C'.format(time))

        # Ensure value between 0 and 9999
        time = int(time+0.5)
        if time > 9999:
            print('Time out of range, set to 9999')
            time = 9999

        # Determine increase to each figure
        thou = divmod(time,1000)[0]
        time = divmod(time,1000)[1]
        hund = divmod(time,100)[0]
        time = divmod(time,100)[1]
        tens = divmod(time,10)[0]
        dig = divmod(time,10)[1]

        # Set time
        self.press_set(2)
        self.press_inc(dig)
        self.press_shift()
        self.press_inc(tens)
        self.press_shift()
        self.press_inc(hund)
        self.press_shift()
        self.press_inc(thou)
        self.press_set()


    # Increase or decrease temperature or time by specified amount
    def change_settings(self, temp_or_time, inc_or_dec, num):
        if temp_or_time == 1:
            temp = True
            num = int(temp*10+0.5)
        elif temp_or_time == 0:
            temp = False
            num = int(num+0.5)
        else:
            print("Invalid entry for temp_or_time: {}".format(temp_or_time))
            return

        if inc_or_dec == 1:
            inc = True
        elif inc_or_dec == 0:
            inc = False
        else:
            print("Invalid entry for inc_or_dec: {}".format(inc_or_dec))
            return   

        # Determine increase or decrease to each figure
        thou = divmod(num,1000)[0]
        num = divmod(num,1000)[1]
        hund = divmod(num,100)[0]
        num = divmod(num,100)[1]
        tens = divmod(num,10)[0]
        dig = divmod(num,10)[1]
   
        # Change setting
        if temp == True:
            self.press_set()
        else:
            self.press_set(2)
        
        if inc  == True:
            self.press_inc(dig)
            self.press_shift()
            self.press_inc(tens)
            self.press_shift()
            self.press_inc(hund)
            if temp == False:
                self.press_shift()
                self.press_inc(thou)
        else:
            self.press_dec(dig)
            self.press_shift()
            self.press_dec(tens)
            self.press_shift()
            self.press_dec(hund)
            if temp == False:
                self.press_shift()
                self.press_dec(thou)

        if temp ==  True:
            self.press_set(2)
        else:
            self.press_set()


