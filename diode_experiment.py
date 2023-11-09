class DiodeExperiment():
    def __init__(self):
        from arduino_device import ArduinoVISADevice
        from arduino_device import list_devices
        port = "ASRL9::INSTR"
        self.device = ArduinoVISADevice(port=port)
    def scan(self, min, max):
        for value in range(min, max):
            self.device.set_output_value(value)
            U_tot = self.device.get_output_value() 
            U_2 = self.device.get_input_value(channel = 2) 
            U_1 = int(U_tot) - int(U_2)
            self.device.U_LED.append(U_1)
            I = int(U_1) / 220
            self.device.I_LED.append(I)
        self.device.set_output_value(0)
        return self.device.U_LED, self.device.I_LED