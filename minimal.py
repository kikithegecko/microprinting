#!/usr/bin/env python

import serial

# initialize printer with given baudrate
printer = serial.Serial("/dev/ttyUSB0", 19200)

# print string (do not forget \n if line is not filled completely)
printer.write("string\n")
