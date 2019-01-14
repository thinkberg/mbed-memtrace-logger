# mbed-memtrace-logger

Analyzes and logs the memtrace output from mbed-os in a readable form. 
This code is left over for the use with micro:bit and Calliope mini.

If you look for the original memtrace, check out the mbed-cli.

> You need to enable heap debug output!

Run with: `python3 memtrace.py /dev/cu.XXXXX 115200`

The script auto-resets the counts and output looks like:
```
HEAP 0: 
heap_start : 0x20002950
heap_end   : 0x20003600
heap_size  : 3248
[F:3248] 
mb_total_free : 3248
mb_total_used : 0
== (001)       56 [20002954] +56     (malloc: ALLOCATED: 56 [0x20002954])
== (002)       76 [20002990] +20     (malloc: ALLOCATED: 20 [0x20002990])
== (003)      124 [200029a8] +48     (malloc: ALLOCATED: 48 [0x200029a8])
...
== (032)     1254 [20002e50] -18     (free:   0x20002e50)
== (031)     1229 [20002ea8] -25     (free:   0x20002ea8)
== (030)     1209 [20002e90] -20     (free:   0x20002e90)
...
Calliope Accelerometer Test v1.0
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
