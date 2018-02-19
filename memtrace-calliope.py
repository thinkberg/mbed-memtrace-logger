"""
A simple mbed memtrace log extractor, calculating allocated memory.

Author: Matthias L. Jugel (@thinkberg)

Prerequisites:
    pip install pygtail

Usage:
    python memtrace.py log-file mem-reset-keyword

    The script will tail the log file and reset the memory counter when
    the mem-reset-keyword occurs.

    a) enable memory tracing in your embedded program (config.json):
    ```
    {
      "microbit-dal": {
        "debug": 1,
        "heap": {
          "debug": 1
        }
      }
    }
    ```

    b) Log into a file:
    `$ miniterm.py /dev/cu.usbmodem142111 9600 | tee memtrace.log`

    c) Analyze log file (tails the log file)
    python -u bin/memtrace.py memtrace.log SHCSR

    If the analyzer behaves strangely, delete the "log-file.offset" file.
"""

import re
import sys

import time

from pygtail import Pygtail

mem = {}
allocated = 0

reset = None
if len(sys.argv) > 1:
    reset = sys.argv[2]
    print "RESETTING tracer on '%s'" % reset

r_malloc = re.compile("^(microbit_)malloc:\\s+(NATIVE\\s+)?(ALLOCATED:)\\s+(\\d+)\\s+\\[(0x[0-9a-f]+)\\]")
r_free = re.compile("^(microbit_)free:\\s+(0x[0-9a-f]+)")

partial = ""
while True:
    for line in Pygtail(sys.argv[1]):
        # we sometimes get incomplete lines, wait for a full line
        if not (line[-1] == '\n' or line[-1] == '\r'):
            partial = line
            continue
        else:
            line = partial + line
            partial = ""

        # strip newline and carriage return
        line = line.rstrip('\n').rstrip('\r')

        # if we detect the reset keyword, rest the map and memory counter
        if reset in line:
            mem = {}
            allocated = 0
            print "\n\n\033[91m>> RESET >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m"

        # match malloc, realloc and free
        m = r_malloc.search(line)
        if m:
            mem[m.group(5)] = int(m.group(4))
            allocated += int(m.group(4))
            print "\033[1m== (%03d) \033[34m%8d\033[0m [%8x] \033[31m+%-6d\033[0m (%s)" % \
                  (len(mem), allocated, allocated, int(m.group(4)),
                   m.group(0).replace(m.group(1), "").replace(m.group(3), ""))
            continue

        m = r_free.search(line)
        if m:
            # print "f", m.group(3)
            freed = 0
            if mem.has_key(m.group(2)):
                freed = mem[m.group(2)]
                allocated -= freed
                del mem[m.group(2)]
            else:
                print "\033[33m!! WARN: free(%s)\033[0m" % m.group(1)
            print "\033[1m== (%03d) \033[34m%8d\033[0m [%8x] \033[92m-%-6d\033[0m (%s)" % \
                  (len(mem), allocated, allocated, freed, m.group(0).replace(m.group(1), ""))
            continue

        # print all other lines as is, so we can still use the log functionality 
        print line
        sys.stdout.flush()
    time.sleep(1)
