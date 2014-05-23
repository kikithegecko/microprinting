#!/usr/bin/env python2
#! -*- coding: utf-8 -*-

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
inputtext = u'abcdefghijklmnopqrstuvwxyzäöüß ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ 1234567890\n'

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

# underlined
newpar()
lp('\x1b\x2d\x01')
lp(inputtext + 'underlined')
lp('\x1b\x2d\x01')

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

# broad font/breitschrift
newpar()
lp('\x1b\x57\x01')
lp(inputtext + 'broad')
lp('\x1b\x57\x00')

# broad and double vertical height
newpar()
lp('\x1b\x77\x01 \x1b\x57\x01')
lp(inputtext + 'borad + vertical')
lp('\x1b\x77\x00 \x1b\x57\x00')

# 10 characters per inch
newpar()
lp('\x1b\x50')
lp(inputtext + '10 CPI')

# 12 characters per inch
newpar()
lp('\x1b\x4d')
lp(inputtext + '12 CPI')

# 15 characters per inch
newpar()
lp('\x1b\x67')
lp(inputtext + '15 CPI')

