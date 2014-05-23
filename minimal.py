#!/usr/bin/env python3

import os, sys

# print string (do not forget \n if line is not filled completely)
os.system("echo " + sys.argv[1] + " > /dev/lp0")
