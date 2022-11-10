import serial
from Logger import Logger
from adafruit_rockblock import RockBlock
from time import sleep
import decode

timeBetweenChecks = 5 #minutes

class Iridium(RockBlock):
    def __init__(self, port="/dev/serial0", baud=19200, debug=False):
        self.logger = Logger("RockBlock", debug)
        self.log("Initiating: ", "Rock Block with " + str(port) + ", " + str(baud) + ", and debugging " + str(debug))
        self.uart = serial.Serial(port, baud)
        super().__init__(self.uart)
        self.log("Model: ", str(self.model))
        self.log("System Time: ", str(self.system_time))
        self.retry = 0
        self.data = ""
        self.msg = {} # Output message that will be accessed from other classes

    def log(self, tag, message):
        log = self.logger
        log.log(tag, message)

    def sq(self):
        sq = self.signal_quality
        self.log("Signal Quality: ", sq)
        return sq

    def available(self):
        return self.uart.in_waiting

    def read(self):
        self.data = self.uart.readline()
        return self.data

    def receive(self):
        self.data = self.data_in
        # self.retry = 0
        return self.data

    def check_signal_status(self):
        return self.satellite_transfer()

    def check_messages(self):
        if self.available() > 0:
            temp_message = {}
            while self.available() > 0:
                temp = self.receive()
                # temp = self.read()
                temp_message.append(decode.decode(temp))
            return temp_message

    def mainloop(self):
        while True:
            self.msg = self.check_messages()
            sleep(timeBetweenChecks * 60)

    def send(self, msg):
        self.log("Message: ", msg)
        self.data_out(msg)

    def write(self, msg):
        self.log("Message: ", msg)
        self.uart.write(msg)

