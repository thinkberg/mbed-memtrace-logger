# mbed-memtrace-logger
Analyzes and los the memtrace output from mbed-os in a readable form. 

The memory trace outputs pretty unreadable information:

```
#m:0x20003080;0x182f-50
#f:0x0;0x183f-0x20003080
#m:0x20003080;0x182f-50
#f:0x0;0x183f-0x20003080
#m:0x20003080;0x182f-50
#f:0x0;0x183f-0x20003080
```

The script takes those lines and converts them into a little more readable
information and also calculates the currently allocated heap:

```
== 00000050 bytes +50     (#m:0x20003080;0x182f-50)
== 00000000 bytes -50     (#f:0x0;0x183f-0x20003080)
== 00000050 bytes +50     (#m:0x20003080;0x182f-50)
== 00000000 bytes -50     (#f:0x0;0x183f-0x20003080)
== 00000050 bytes +50     (#m:0x20003080;0x182f-50)
== 00000000 bytes -50     (#f:0x0;0x183f-0x20003080)
```

Even in color :-)
![logoutput.png](logoutput.png)

# Using a log file
- enable memory tracing in your mbed program
- log uart output into a file
- run script to analyze memory state

# Using a stream
- enable memory tracing in your mbed program
- log uart into a log file continuously: `miniterm.py /dev/cu.usbmodem1234 9600 | tee memtrace.log`
- run script to tail file `python memtrace.py memtrace.log KEYWORD`

Enjoy!
