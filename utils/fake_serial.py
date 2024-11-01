# fakeSerial.py
# D. Thiebaut
# A very crude simulator for PySerial assuming it
# is emulating an Arduino.

# a Serial class emulator

import logging

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
PARITY_NONE = 'N'


class Serial:

    # init(): the constructor.  Many of the arguments have default values
    # and can be skipped when calling the constructor.
    def __init__(self, port='COM1', baudrate=19200, timeout=1,
                 bytesize=8, parity='N', stopbits=1, xonxoff=0,
                 rtscts=0, write_timeout=1):
        self.name = port
        self.port = port
        self.timeout = timeout
        self.parity = parity
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self._isOpen = True
        self._receivedData = b""
        self.write_timeout = write_timeout
        self._data = b"It was the best of times.\nIt was the worst of times.\n"

    # isOpen()
    # returns True if the port to the Arduino is open.  False otherwise
    def is_open(self):
        return self._isOpen

    def reset_input_buffer(self):
        self._data = b""

    def reset_output_buffer(self):
        self._receivedData = b""

    # open()
    # opens the port
    def open(self):
        self._isOpen = True

    # close()
    # closes the port
    def close(self):
        self._isOpen = False

    # write()
    # writes a string of characters to the Arduino
    def write(self, string):
        logger.info(f"Writing to serial: {string}")
        self._receivedData += string

    # read()
    # reads n characters from the fake Arduino. Actually n characters
    # are read from the string _data and returned to the caller.
    def read(self, n=1):
        dt = self._data[0:n]
        self._data = self._data[n:]
        logger.info(f"Received from serial: {self._data}")
        return dt

    # readline()
    # reads characters from the fake Arduino until a \n is found.
    def readline(self):
        returnIndex = self._data.index("\n")
        if returnIndex != -1:
            s = self._data[0:returnIndex + 1]
            self._data = self._data[returnIndex + 1:]
            return s
        else:
            return ""

    # __str__()
    # returns a string representation of the serial class
    def __str__(self):
        return "Serial<id=0xa81c10, open=%s>( port='%s', baudrate=%d," \
               % (str(self.isOpen), self.port, self.baudrate) \
            + " bytesize=%d, parity='%s', stopbits=%d, xonxoff=%d, rtscts=%d)"\
               % (self.bytesize, self.parity, self.stopbits, self.xonxoff,
                   self.rtscts)
