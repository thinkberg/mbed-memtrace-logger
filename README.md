# mbed-memtrace-logger

Analyzes and logs the memtrace output from mbed-os in a readable form. 
This code is left over for the use with micro:bit and Calliope mini.

If you look for the original memtrace, check out the mbed-cli.

> You need to enable heap debug output!

Run with: `python3 memtrace.py /dev/cu.XXXXX 115200`

To make full use of this script, configure your microbit-dal as follows:

```json
{
	"microbit-dal": {
		"debug": 1,
		"heap_debug": 1,
		"panic_on_heap_full": 1
	}
}
```

The script auto-resets the counts and output looks like:
```
HEAP 0: 
heap_start : 0x20002950
heap_end   : 0x20003800
heap_size  : 3760

>> RESET HEAP COUNTERS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   (NUM)    FREE  [ ADDRESS] CHANGE  (COMMENT)
[F:3760] 
mb_total_free : 3760
mb_total_used : 0
== (001)     3704 [20002954] +56     (malloc: ALLOCATED: 56 [0x20002954])
== (002)     3684 [20002990] +20     (malloc: ALLOCATED: 20 [0x20002990])
== (003)     3636 [200029a8] +48     (malloc: ALLOCATED: 48 [0x200029a8])
...
== (025)     2815 [20002d50] +24     (malloc: ALLOCATED: 24 [0x20002d50])
== (026)     2591 [20002d6c] +224    (malloc: ALLOCATED: 224 [0x20002d6c])
== (025)     2615 [20002d50] -24     (free:   0x20002d50)
!! (025) WARN: free(0x0)
== (025)     2615 [       0] -0      (free:   0)
...
== (039)     1438 [20002ec0] +31     (malloc: ALLOCATED: 31 [0x20002ec0])
== (038)     1478 [200032f4] -40     (free:   0x200032f4)
== (037)     1509 [20002ec0] -31     (free:   0x20002ec0)
== (038)     1081 [200032f4] +428    (malloc: ALLOCATED: 428 [0x200032f4])
!! (038) : malloc(): no free block of size 1024
HEAP ALLOCATION (% header | * data | . free)
000000 20002950 %%%%********************************************************%%%%
000064 20002990 ********************%%%%****************************************
...
001280 20002e50 ********%%%%********%%%%********************................%%%%
001344 20002e90 ********************%%%%********************....................
001408 20002ed0 ....................%%%%****************************************
001472 20002f10 ****************************************************************
...
== Free blocks: ==
20002e7c 16 bytes
20002ebc 40 bytes
200034a0 864 bytes
```

## License

```
Copyright 2018 Matthias L. Jugel (@thinkberg)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
