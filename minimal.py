#!/usr/bin/env python3

import os, sys

# print string
output = 'echo "' + sys.argv[1] + '" > /dev/lp0'
output = output.encode('cp437', 'replace')
os.system(output)
