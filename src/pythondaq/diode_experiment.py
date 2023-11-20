import numpy as np
import statistics
from pythondaq.arduino_device import ArduinoVISADevice, list_devices

# Deze class stuurt een spanning door een elektrisch circuit 
# en meet de spanning over en de stroomsterkte door een LED
class DiodeExperiment():

    # Deze method bewaart alle hergebruikte informatie
    def __init__(self):
        port = "ASRL9::INSTR"
        self.device = ArduinoVISADevice(port=port)

        # Deze lijsten slaan de spanning en stroomsterkte apart en samen op
        self.U_LED = []
        self.I_LED = []

        self.I_temp = []
        self.standaard_deviaties_I =[]
        self.gemidelde_I = []
        
        self.U_temp = []
        self.standaard_deviaties_U = []
        self.gemiddelde_U = []
    # Deze method voert het experiment uit
    def scan(self, min, max, N):
        for value in range(min, max):
            self.device.set_output_value(value)

            self.I_temp = []
            self.U_temp = []
            for herhaling in range(N):   
                U_totaal = self.device.get_input_voltage(channel = 1) 
                U_weerstand = self.device.get_input_voltage(channel = 2) 
                U_LED = U_totaal - U_weerstand
                I = U_weerstand / 220
                self.I_temp.append(I)
                self.U_temp.append(U_LED)
            
            gem_I = statistics.mean(self.I_temp)
            std_I = np.std(self.I_temp)/(N**0.5)
            
            self.standaard_deviaties_I.append(std_I)
            self.gemidelde_I.append(gem_I) 

            gem_U = statistics.mean(self.U_temp)
            std_U = np.std(self.U_temp)/(N**0.5)

            self.standaard_deviaties_U.append(std_U)
            self.gemiddelde_U.append(gem_U)


        self.device.set_output_value(0)
        return self.standaard_deviaties_I, self.gemidelde_I, self.standaard_deviaties_U, self.gemiddelde_U