#!/usr/bin/env python3

import sys

# print string
lp = open('/dev/lp0', 'wb')
output = sys.argv[1] + '\n'
output = output.encode('cp437', 'replace')
lp.write(output)

