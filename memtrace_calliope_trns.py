# mbed debug trace transformer, handling memory trace information
# Author: Matthias L. Jugel (@thinkberg)
#
# Copyright (c) 2018 ubirch GmbH, All Rights Reserved
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied.

import re
import sys

from serial.tools.miniterm import Transform

def debug(s):
    sys.stderr.write("D "+repr(s)+"\r\n")

class CalliopeDebugTransform(Transform):
    mem = {}
    allocated = 0
    reset = None
    buffer = ""

    def __init__(self):
        self.r_malloc = re.compile("(?:microbit_)?malloc:\s+(?:NATIVE\s+)?(?:ALLOCATED:)\s+(\d+)\s+\[(0x[0-9a-f]+)\]")
        self.r_free = re.compile("^(?:microbit_)?free:\\s+(0x[0-9a-f]+)")
        self.r_heap_size = re.compile("^mb_total_free : (\d+)")

    def rx(self, rx_input):
        # collect lines
        out = ""
        for c in rx_input:
            if c == '\r' or c == '\n':
                if len(self.buffer):
                    out += self.trace_line(self.buffer)
                else:
                    out += "\n"
                self.buffer = ""
                continue
            else:
                self.buffer += c
                continue
        return out

    def trace_line(self, line):
        # strip newline and carriage return
        line = line.rstrip('\n').rstrip('\r')

        m = self.r_heap_size.search(line)
        if m:
            self.max = int(m.group(1))
            self.mem = {}
            self.allocated = 0
            line += "\r\n\r\n\033[91m>> RESET HEAP COUNTERS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m\r\n"
            line += "\033[4m   (NUM)    TOTAL [ ADDRESS] CHANGE  (COMMENT)\033[0m\r\n"
            return line

        # match malloc, realloc and free
        m = self.r_malloc.search(line)
        if m:
            out = ""
            if m.group(2) == "0":
                out += "\033[1m!! (%03d) \033[31mmalloc failed\033[0m (%s)\r\n" % (len(self.mem), line)
            else:
                self.mem[m.group(2)] = int(m.group(1))
                self.allocated += int(m.group(1))
                out += "\033[1m== (%03d) \033[34m%8d\033[0m [%8x] \033[31m+%-6d\033[0m (%s)\r\n" % \
                       (len(self.mem), self.allocated, int(m.group(2), 16), int(m.group(1)), line)
                return out

        m = self.r_free.search(line)
        if m:
            out = ""
            freed = 0
            if m.group(1) in self.mem:
                freed = self.mem[m.group(1)]
                self.allocated -= freed
                del self.mem[m.group(1)]
            else:
                out += "\033[33m!! (%03d) WARN: free(0x%s)\033[0m\r\n" % (len(self.mem), m.group(4))
            out += "\033[1m== (%03d) \033[34m%8d\033[0m [%8x] \033[92m-%-6d\033[0m (%s)\r\n" % \
                   (len(self.mem), self.allocated, int(m.group(1), 16), freed, line)
            return out

        # print all other lines as is, so we can still use the log functionality
        return line + "\r\n"
