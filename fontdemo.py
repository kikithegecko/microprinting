#!/usr/bin/env python2

""" Prints different fonts in various configurations. """

import serial

# initialize printer with given  baudrate
printer = serial.Serial("/dev/ttyUSB0", 19200)

# set input text
inputtext = "abcdefghijklmnopqrstuvwxyz\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n1234567890\n"

# normal
printer.write("\x1b\x21\x00")
printer.write(inputtext + "48 chars per line\n\n\n")

# double height
printer.write("\x1b\x21\x10")
printer.write(inputtext + "48 chars per line\n\n\n")

# double width
printer.write("\x1b\x21\x20")
printer.write(inputtext + "24 chars per line\n\n\n")


# double width and double height
printer.write("\x1b\x21\x30")
printer.write(inputtext + "24 chars per line\n\n\n")

# reset
printer.write("\x1b\x7B\0")

printer.write("------------------------\n\n\n")

# normal
printer.write("\x1b\x21\x01")
printer.write(inputtext + "64 chars per line\n\n\n")

# double height
printer.write("\x1b\x21\x11")
printer.write(inputtext + "64 chars per line\n\n\n")

# double width
printer.write("\x1b\x21\x21")
printer.write(inputtext + "32 chars per line\n\n\n")


# double width and double height
printer.write("\x1b\x21\x31")
printer.write(inputtext + "32 chars per line\n\n\n")

# reset
printer.write("\x1b\x7B\0")
