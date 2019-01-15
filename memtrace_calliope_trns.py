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
    max = 0
    allocated = 0
    reset = None
    buffer = ""

    def __init__(self):
        self.r_malloc = re.compile("(?:microbit_)?malloc:\s+(?:NATIVE\s+)?(?:ALLOCATED:)\s+(\d+)\s+\[(0x[0-9a-f]+)\]")
        self.r_free = re.compile("^(?:microbit_)?free:\\s+((0x)?[0-9a-f]+)")
        self.r_heap_start = re.compile("^heap_start\s+:\s+(0x[0-9a-f]+)")
        self.r_heap_end = re.compile("^heap_end\s+:\s+(0x[0-9a-f]+)")
        self.r_heap_size = re.compile("^heap_size\s+:\s+(\d+)")
        self.r_oom = re.compile("^malloc:\s+OUT OF MEMORY\s+\[(\d+)\]")

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


    def colorize(self, free):
        if free > self.max/2: return "4"
        elif free > self.max/3: return "5"
        return "1"

    def trace_line(self, line):
        # strip newline and carriage return
        line = line.rstrip('\n').rstrip('\r')

        m = self.r_heap_size.search(line)
        if m:
            self.max = int(m.group(1))
            self.mem = {}
            self.allocated = 0
            line += "\r\n\r\n\033[91m>> RESET HEAP COUNTERS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m\r\n"
            line += "\033[4m   (NUM)    FREE  [ ADDRESS] CHANGE  (COMMENT)\033[0m\r\n"
            return line

        m = self.r_heap_start.search(line)
        if m:
            self.heap_start = int(m.group(1), 16)
            return line + "\r\n"

        m = self.r_heap_end.search(line)
        if m:
            self.heap_end = int(m.group(1), 16)
            return line + "\r\n"

        # match malloc, realloc and free
        m = self.r_malloc.search(line)
        if m:
            out = ""
            if m.group(2) == "0":
                out += "\033[1m!! (%03d) \033[31mmalloc failed\033[0m (%s)\r\n" % (len(self.mem), line)
            else:
                addr = int(m.group(2), 16)
                self.mem[addr] = int(m.group(1))
                self.allocated += int(m.group(1))
                free = self.max - self.allocated
                out += "\033[1m== (%03d) \033[3%sm%8d\033[0m [%8x] \033[31m+%-6d\033[0m (%s)\r\n" % \
                       (len(self.mem), self.colorize(free), free, addr, int(m.group(1)), line)
                return out

        m = self.r_free.search(line)
        if m:
            out = ""
            freed = 0
            addr = int(m.group(1), 16)
            if addr in self.mem:
                freed = self.mem[addr]
                self.allocated -= freed
                del self.mem[addr]
            else:
                out += "\033[33m!! (%03d) WARN: free(0x%x)\033[0m\r\n" % (len(self.mem), addr)

            free = self.max - self.allocated
            out += "\033[1m== (%03d) \033[3%sm%8d\033[0m [%8x] \033[92m-%-6d\033[0m (%s)\r\n" % \
                   (len(self.mem), self.colorize(free), free, addr, freed, line)
            return out

        m = self.r_oom.search(line)
        if m:
            out = ""
            wanted = int(m.group(1))
            out += "\033[31m!! (%03d) : malloc(): no free block of size %d\033[0m\r\n" % (len(self.mem), wanted)


            mem = ""
            end = 0
            for addr in range(self.heap_start, self.heap_end):
                if addr+4 in self.mem:
                    start = addr+4
                    end = addr+4 + self.mem[addr+4]
                if addr == end:
                    end = 0
                if end:
                    if addr < start: mem += "%"
                    else: mem += "*"
                else:
                    mem += "."

            out += "HEAP ALLOCATION (% header | * data | . free)\r\n"
            for a in range(0, self.max, 64):
                out += "%06d %08x %s\r\n" % (a, self.heap_start + a, mem[a:a+64])

            addr = 0
            out += "\033[31m== Free blocks: ==\033[0m\r\n"
            blocks = re.findall("[%*]+|[.]+", mem)
            for b in blocks:
                if len(b) > 4 and b[0] == '.':
                    out += "%08x %d bytes\r\n" % (self.heap_start + addr, len(b))
                addr += len(b)

            return out

        # print all other lines as is, so we can still use the log functionality
        return line + "\r\n"
