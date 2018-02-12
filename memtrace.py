"""
A simple mbed memtrace log extractor, calculating allocated memory.

Author: Matthias L. Jugel (@thinkberg)

Prerequisites:
    pip install pygtail

Usage:
    python memtrace.py log-file mem-reset-keyword

    The script will tail the log file and reset the memory counter when
    the mem-reset-keyword occurs.

    a) enable memory tracing in your embedded program:
    ```
    #ifdef MBED_MEM_TRACING_ENABLED
      mbed_mem_trace_set_callback(mbed_mem_trace_default_callback);
    #endif
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


r_malloc = re.compile("#m:(0x[0-9a-f]+);(0x[0-9a-f]+)-(\\d+)")
r_realloc = re.compile("#r:(0x[0-9a-f]+);(0x[0-9a-f]+)-(0x[0-9a-f]+);(\\d+)")
r_free = re.compile("#f:(0x[0-9a-f]+);(0x[0-9a-f]+)-(0x[0-9a-f]+)")

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
            # print "m", m.group(1), ":", m.group(3)
            mem[m.group(1)] = int(m.group(3))
            allocated += int(m.group(3))
            print "\033[1m== \033[34m%08d\033[0m bytes, \033[31m+%-6d\033[0m (%s)" % (allocated, int(m.group(3)), line)
            continue

        m = r_realloc.search(line)
        if m:
            # print "r", m.group(1), ":", m.group(4)
            diff = 0
            if mem.has_key(m.group(1)):
                diff = int(m.group(4)) - mem[m.group(1)]
                mem[m.group(1)] = int(m.group(4))
            else:
                print "!! WARN: realloc() without previous allocation!"
                print "!! WARN: %s" % line
            allocated += diff
            print "\033[1m== \033[34m%08d\033[0m bytes \033[35m+%-6d\033[0m (%s)" % (allocated, diff, line)
            continue

        m = r_free.search(line)
        if m:
            # print "f", m.group(3)
            freed = 0
            if mem.has_key(m.group(3)):
                freed = mem[m.group(3)]
                allocated -= freed
                del mem[m.group(3)]
            else:
                print "!! WARN: free(%s)" % m.group(3)
            print "\033[1m== \033[34m%08d\033[0m bytes \033[92m-%-6d\033[0m (%s)" % (allocated, freed, line)
            continue

        # print all other lines as is, so we can still use the log functionality 
        print line
        sys.stdout.flush()
    time.sleep(1)
