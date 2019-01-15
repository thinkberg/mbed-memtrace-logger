# mbed-memtrace-logger

Analyzes and logs the memtrace output from mbed-os in a readable form. 
This code is left over for the use with micro:bit and Calliope mini.

If you look for the original memtrace, check out the mbed-cli.

> You need to enable heap debug output!

Run with: `python3 memtrace.py /dev/cu.XXXXX 115200`

The script auto-resets the counts and output looks like:
```
>> RESET HEAP COUNTERS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   (NUM)    TOTAL [ ADDRESS] CHANGE  (COMMENT)
[F:3760] 
mb_total_free : 3760
mb_total_used : 0
== (001)     3704 [20002954] +56     (malloc: ALLOCATED: 56 [0x20002954])
== (002)     3684 [20002990] +20     (malloc: ALLOCATED: 20 [0x20002990])
== (003)     3636 [200029a8] +48     (malloc: ALLOCATED: 48 [0x200029a8])
== (004)     3620 [200029dc] +16     (malloc: ALLOCATED: 16 [0x200029dc])
== (005)     3580 [200029f0] +40     (malloc: ALLOCATED: 40 [0x200029f0])
== (006)     3556 [20002a1c] +24     (malloc: ALLOCATED: 24 [0x20002a1c])
== (007)     3516 [20002a38] +40     (malloc: ALLOCATED: 40 [0x20002a38])
== (008)     3492 [20002a64] +24     (malloc: ALLOCATED: 24 [0x20002a64])
== (009)     3484 [20002a80] +8      (malloc: ALLOCATED: 8 [0x20002a80])
== (010)     3476 [20002a8c] +8      (malloc: ALLOCATED: 8 [0x20002a8c])
== (011)     3384 [20002a98] +92     (malloc: ALLOCATED: 92 [0x20002a98])
== (012)     3376 [20002af8] +8      (malloc: ALLOCATED: 8 [0x20002af8])
== (013)     3368 [20002b04] +8      (malloc: ALLOCATED: 8 [0x20002b04])
== (014)     3256 [20002b10] +112    (malloc: ALLOCATED: 112 [0x20002b10])
== (015)     3216 [20002b84] +40     (malloc: ALLOCATED: 40 [0x20002b84])
== (016)     3192 [20002bb0] +24     (malloc: ALLOCATED: 24 [0x20002bb0])
== (017)     3179 [20002bcc] +13     (malloc: ALLOCATED: 13 [0x20002bcc])
== (018)     3087 [20002be0] +92     (malloc: ALLOCATED: 92 [0x20002be0])
== (019)     2995 [20002c40] +92     (malloc: ALLOCATED: 92 [0x20002c40])
== (020)     2955 [20002ca0] +40     (malloc: ALLOCATED: 40 [0x20002ca0])
== (021)     2915 [20002ccc] +40     (malloc: ALLOCATED: 40 [0x20002ccc])
== (022)     2903 [20002cf8] +12     (malloc: ALLOCATED: 12 [0x20002cf8])
== (023)     2863 [20002d08] +40     (malloc: ALLOCATED: 40 [0x20002d08])
== (024)     2839 [20002d34] +24     (malloc: ALLOCATED: 24 [0x20002d34])
== (025)     2815 [20002d50] +24     (malloc: ALLOCATED: 24 [0x20002d50])
== (026)     2591 [20002d6c] +224    (malloc: ALLOCATED: 224 [0x20002d6c])
!! (026) WARN: free(0x0x20002d50)
== (026)     2591 [       0] -0      (free:   0x20002d50)
== (026)     2581 [20002d50] +10     (malloc: ALLOCATED: 10 [0x20002d50])
== (027)     2571 [20002e50] +10     (malloc: ALLOCATED: 10 [0x20002e50])
== (028)     2561 [20002e60] +10     (malloc: ALLOCATED: 10 [0x20002e60])
== (029)     2546 [20002e70] +15     (malloc: ALLOCATED: 15 [0x20002e70])
!! (029) WARN: free(0x0x20002e60)
== (029)     2546 [       0] -0      (free:   0x20002e60)
!! (029) WARN: free(0x0x20002e50)
== (029)     2546 [       0] -0      (free:   0x20002e50)
== (029)     2528 [20002e50] +18     (malloc: ALLOCATED: 18 [0x20002e50])
== (030)     2521 [20002d60] +7      (malloc: ALLOCATED: 7 [0x20002d60])
== (031)     2515 [20002e84] +6      (malloc: ALLOCATED: 6 [0x20002e84])
== (032)     2495 [20002e90] +20     (malloc: ALLOCATED: 20 [0x20002e90])
== (033)     2470 [20002ea8] +25     (malloc: ALLOCATED: 25 [0x20002ea8])
== (034)     2444 [20002ec8] +26     (malloc: ALLOCATED: 26 [0x20002ec8])
!! (034) WARN: free(0x0x20002e50)
== (034)     2444 [       0] -0      (free:   0x20002e50)
!! (034) WARN: free(0x0x20002ea8)
== (034)     2444 [       0] -0      (free:   0x20002ea8)
!! (034) WARN: free(0x0x20002e90)
== (034)     2444 [       0] -0      (free:   0x20002e90)
== (034)     2436 [20002e50] +8      (malloc: ALLOCATED: 8 [0x20002e50])
== (035)     2116 [20002ee8] +320    (malloc: ALLOCATED: 320 [0x20002ee8])
== (036)     2108 [20002e5c] +8      (malloc: ALLOCATED: 8 [0x20002e5c])
== (036)     2088 [20002e90] +20     (malloc: ALLOCATED: 20 [0x20002e90])
== (037)     1476 [2000302c] +612    (malloc: ALLOCATED: 612 [0x2000302c])
== (037)     1456 [20002ea8] +20     (malloc: ALLOCATED: 20 [0x20002ea8])
== (038)     1436 [20003294] +20     (malloc: ALLOCATED: 20 [0x20003294])
== (039)     1400 [200032ac] +36     (malloc: ALLOCATED: 36 [0x200032ac])
!! (039) WARN: free(0x0x20002e84)
== (039)     1400 [       0] -0      (free:   0x20002e84)
!! (039) WARN: free(0x0x20002d60)
== (039)     1400 [       0] -0      (free:   0x20002d60)
!! (039) WARN: free(0x0x20002ec8)
== (039)     1400 [       0] -0      (free:   0x20002ec8)
!! (039) WARN: free(0x0x20002e70)
== (039)     1400 [       0] -0      (free:   0x20002e70)
== (040)     1365 [20002e68] +35     (malloc: ALLOCATED: 35 [0x20002e68])
== (041)     1344 [20002ec0] +21     (malloc: ALLOCATED: 21 [0x20002ec0])
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
