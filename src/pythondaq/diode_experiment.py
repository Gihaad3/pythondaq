import numpy as np
import statistics
from pythondaq.arduino_device import ArduinoVISADevice
from pythondaq.arduino_device import list_devices
from statistics import mean

# Deze class stuurt een spanning door een elektrisch 
# circuit en meet de spanning over en de stroomsterkte door 
# een LED
class DiodeExperiment():

    # Deze method bewaart alle hergebruikte informatie
    def __init__(self):
        port = "ASRL9::INSTR"
        self.device = ArduinoVISADevice(port=port)

        # Deze lijsten slaan de spanning en stroomsterkte
        # apart en samen op
        self.U_LED = []
        self.I_LED = []
        self.U_I = []

    # Deze method voert het experiment uit
    def scan(self, min, max):
        for value in range(min, max):
            self.device.set_output_value(value)
            U_totaal = self.device.get_input_voltage(channel = 0) 
            U_weerstand = self.device.get_input_voltage(channel = 2) 
            U_lamp = int(U_totaal) - int(U_weerstand)
            self.U_LED.append(U_lamp)
            I = int(U_weerstand) / 220
            self.I_LED.append(I)
            self.U_I.append([U_lamp, I])
        self.device.set_output_value(0)
        return self.U_LED, self.I_LED, self.U_I