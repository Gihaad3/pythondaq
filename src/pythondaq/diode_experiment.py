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
        self.U_I = []
        self.alle_data =[]
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

    # Deze method voert het experiment een aantal keer 
    # uit en slaat alle data op in één lijst
    def runexperiment(self, herhalingen, min, max):
        self.alle_data = []

	    #Ik herhaal het experiment en gebruik daarbij de nested list met U en I
        for i in range(herhalingen):
            experiment = DiodeExperiment.scan(self, min, max)[2]
		   
            #Ik ga elke waarde af in een individueel experiment en stop het in één lijst
            for waarde in experiment:
                self.alle_data.append(waarde)
        return self.alle_data  

    #Deze method berekent de standaard deviatie
    def std_calc(self,min,max):
        standaard_deviaties = []
        gemidelde_I = []
	
	    #Ik ga de spannings interval af
        for volt in range(min,max):

	        # Ik zet de lijst met stroomsterktes telkens op nul
            I_lijst = []
		    # Ik ga elke waarde af in de complete set
            # van de herhaalde experimenten
            for waarde in self.alle_data:
	        
            # waarde is in dit geval een lijst met spanning en stroomsterkte
		    # Ik sorteer de lijst hier, ik ga elke spanningswaarde
            # af en zet de bijberhornde stroomsterkte in een lijst
                if waarde[0] == volt:
                    I_lijst.append(waarde[1])
		    
            # Ik bereken het gemidelde en de standaard deviatie
            gem_I = statistics.mean(I_lijst)
            std_I = np.std(I_lijst)
            standaard_deviaties.append(std_I)
            gemidelde_I.append(gem_I)
        return gemidelde_I, standaard_deviaties