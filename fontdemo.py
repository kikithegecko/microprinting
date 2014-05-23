#!/usr/bin/env python3

""" Prints different fonts in various configurations. """

import os
import struct

def lp(text):
   prtr = open('/dev/lp0', 'wb')
   txt = text + '\n'
   prtr.write(txt.encode('cp437', 'replace'))
   prtr.close()

def newpar():
   # LF LF CR
   lp('\x0a\x0a\x0d')

# set input text
inputtext = "abcdefghijklmnopqrstuvwxyzäöüß ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ 1234567890"

# normal
newpar()
lp(inputtext + 'normal')

# italic
newpar()
lp('\x1b\x34')
lp(inputtext + 'italic')
lp('\x1b\x35')

# shadow font!/schattenschrift
newpar()
lp('\x1b\x45')
lp(inputtext + 'shadow')
lp('\x1b\x46')

# bold font
newpar()
lp('\x1b\x47')
lp(inputtext + 'bold')
lp('\x1b\x48')

# monospace
newpar()
lp('\x1b\x70\x01')
lp(inputtext + 'monospace')
lp('\x1b\x70\x00')

# vertical height doubled
newpar()
lp('\x1b\x77\x01')
lp(inputtext + 'vertical')
lp('\x1b\x77\x00')

