"""
Trying to talk to the BNO055 over UART...
"""
import time
import sys

import serial
import RPi.GPIO as gpio


class FlightSimulator(object):
    
    def __init__(self):
        self.reset_pin = 26
        
        self.ser = serial.Serial("/dev/serial0", 115200)
    
    def set_mode_to_imu(self):
        self.ser.write(bytearray.fromhex('AA003D0108'))
        
    def initialize(self):
        self.set_reset_pin()
        self.reset_bno()
        if self.ser.is_open == False:
            self.ser.open()
        self.set_mode_to_imu()
        if self.get_confirmation() != bytearray.fromhex('EE01'):
            sys.exit(1)
        self.calibrate()

    def reset_bno(self):
        print("resetting")
        gpio.output(self.reset_pin, 0)
        gpio.output(self.reset_pin, 1)
        time.sleep(.5)
        
    def set_reset_pin(self):
        reset_pin = 26

        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(reset_pin, gpio.OUT)
        
    def get_confirmation(self):
        response = self.ser.read(2)
        if response == bytearray.fromhex('EE01'):
            print("BNO055 Ready!")
        return response

    def calibrate(self):
        print("Calibrating...")
        self.ser.write(bytearray.fromhex('AA013501'))
        status = self.ser.read(1)
        message = self.ser.read(1)
        if status + message != bytearray.fromhex('BB01'):
            print("Got error reading Calibration: {}{}".format(status, message))
            return
        print("Calibration status is Good!")

    def read_accl_x(self):
        """
        TODO: This is reading data, but not very well...
        What I need to do is write the request, then expect a BB, then read byte length, then read data
        """
        self.ser.write(bytearray.fromhex('AA010901'))
        status = self.ser.read(1)
        if status != bytearray.fromhex('BB'):
            message = self.ser.read(1)
            print("Got error reading MSB: {}{}".format(status, message))
            return
        length = self.ser.read(1)
        for dat in range(int.from_bytes(length, byteorder='big')):
            msb = self.ser.read(1)
        
        self.ser.write(bytearray.fromhex('AA010801'))
        status = self.ser.read(1)
        if status != bytearray.fromhex('BB'):
            message = self.ser.read(1)
            print("Error reading LSB: {}{}".format(status, message))
            return
        length = self.ser.read(1)
        for dat in range(int.from_bytes(length, byteorder='big')):
            lsb = self.ser.read(1)

        return msb + lsb
        
if __name__ == '__main__':
    fs = FlightSimulator()
    fs.initialize()
    print("getting data")
    while True:
        time.sleep(3)
        print("ACCL X: {}".format(fs.read_accl_x()))
        
