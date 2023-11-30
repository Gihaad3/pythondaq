import numpy as np
import statistics
from pythondaq.arduino_device import ArduinoVISADevice, list_devices, identification


class DiodeExperiment():
    """This class contains runs the experiment a number of times for a given voltage in units ADC
    """

    
    def __init__(self, port):
        """This method opens the selects the device and srores important values
        """
        # Here the port is slected and uses the controller to open it
        self.device = ArduinoVISADevice(port=port)

        # These are the lists with values regarding the current, I
        self.I_temp = []
        self.standard_deviation_I =[]
        self.average_I = []
        
        # These are the lists with values rtegarding the voltage, U
        self.U_temp = []
        self.standard_deviation_U = []
        self.average_U = []

    
    def scan(self, min, max, N):
        """This method repeats the experiment a number of times over a interval in units ADC and calculates the standard deviation and average

        Returns:
            list: The standard deviation of I, the avergae of I, The standard deviation of U, the avergae of U
        """

        #  I go over an interval in units ADC
        for value in np.arange(min, max, 1):

            # I set the voltage in ADC
            self.device.set_output_value(value)

            # temperary lists for current and voltage
            self.I_temp = []
            self.U_temp = []

            #  I repeat the experiment for every step of the interval
            for herhaling in range(N): 
                
                # I measure the voltage in volts over the entire circuit and the resisctence
                U_total = self.device.get_input_voltage(channel = 1) 
                U_resisctence = self.device.get_input_voltage(channel = 2) 

                # I calculate the voltage and current and add them to lists
                U_LED = U_total - U_resisctence
                I = U_resisctence / 220
                self.I_temp.append(I)
                self.U_temp.append(U_LED)
            
            #  I calculate the standard deviation and averge of the voltage and current
            gem_I = statistics.mean(self.I_temp)
            std_I = np.std(self.I_temp)/(N**0.5)
            
            self.standard_deviation_I.append(std_I)
            self.average_I.append(gem_I) 

            gem_U = statistics.mean(self.U_temp)
            std_U = np.std(self.U_temp)/(N**0.5)

            self.standard_deviation_U.append(std_U)
            self.average_U.append(gem_U)

        #  I turn the LED off
        self.device.set_output_value(0)
        return self.average_U, self.standard_deviation_U, self.average_I, self.standard_deviation_I