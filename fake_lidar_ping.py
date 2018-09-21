"""
This is used to recieve data from the fake lidar thing I bought.  Don't remember the name.
It has a stick what says "U030021 8011124" on the top of it.  Don't remember what pins I used... Have fun future me!
"""

import serial

ser = serial.Serial("/dev/serial0", 115200)


def initialize():
    """Not sure if this is needed..."""
    #ser.write(0x42)
    ser.write(bytes(b'B'))

    #ser.write(0x57)
    ser.write(bytes(b'W'))

    #ser.write(0x02)
    ser.write(bytes(2))

    #ser.write(0x00)
    ser.write(bytes(0))

    #ser.write(0x00)
    ser.write(bytes(0))

    #ser.write(0x00)
    ser.write(bytes(0))
              
    #ser.write(0x01)
    ser.write(bytes(1))
              
    #ser.write(0x06)
    ser.write(bytes(6))


def getTFminiData():
    error = 5
    while True:
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            ser.reset_input_buffer()
            # print(type(recv[0]))
            # print(recv[1])
            # print(recv[2])
            if chr(recv[0]) == 'Y' and chr(recv[1]) == 'Y': # 0x59 is 'Y'
                low = recv[2]
                high = recv[3]
                distance = low + high * 256 + error
                print(distance)
                


if __name__ == '__main__':
    try:
        if ser.is_open == False:
            ser.open()
        initialize()
        print("getting data")
        getTFminiData()
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()