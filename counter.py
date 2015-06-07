#!/usr/bin/python

import sys
import time

counter=0
label = sys.argv[1]

while True:
    print('%s: %i' % (label,counter))
    counter += 1
    time.sleep(1)
