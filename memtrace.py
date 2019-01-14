import sys

from memtrace_calliope_trns import CalliopeDebugTransform


class TraceTerminal(object):
    serial = None # Serial() object
    port = None
    baudrate = None
    echo = None

    def __init__(self, port, baudrate=9600, echo=True, timeout=10):
        self.port = port
        self.baudrate = int(baudrate)
        self.timeout = int(timeout)
        self.echo = False if str(echo).lower() == 'off' else True

        try:
            from serial import Serial, SerialException
            self.serial = Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)
            self.serial.flush()
            self.serial.reset_input_buffer()
        except (IOError, ImportError, OSError, Exception):
            self.serial = None
            return

    def terminal(self):
        try:
            import serial.tools.miniterm as miniterm
        except (IOError, ImportError, OSError) as e:
            print(repr(e))
            return False

        term = miniterm.Miniterm(self.serial, echo=self.echo)
        term.exit_character = '\x03'
        term.menu_character = '\x14'
        term.set_rx_encoding('UTF-8')
        term.set_tx_encoding('UTF-8')

        term.rx_transformations += [CalliopeDebugTransform()]

        term.start()

        try:
            term.join(True)
        except KeyboardInterrupt:
            pass
        term.join()
        term.close()

term = TraceTerminal(sys.argv[1], int(sys.argv[2])).terminal()


