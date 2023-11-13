import numpy as np
import statistics
from arduino_device import ArduinoVISADevice
from arduino_device import list_devices

class DiodeExperiment():
    def __init__(self):
        port = "ASRL9::INSTR"
        self.device = ArduinoVISADevice(port=port)
        self.U_LED = []
        self.I_LED = []
        self.U_af = []
        self.I_af = []
    def scan(self, min, max):
        for value in range(min, max):
            self.device.set_output_value(value)
            U_tot = self.device.get_output_value() 
            U_2 = self.device.get_input_value(channel = 2) 
            U_1 = int(U_tot) - int(U_2)
            self.U_LED.append(U_1)
            I = int(U_1) / 220
            self.I_LED.append(I)
        self.device.set_output_value(0)
        return self.U_LED, self.I_LED