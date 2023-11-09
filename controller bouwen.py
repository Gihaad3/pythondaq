import pyvisa
import matplotlib.pyplot as plt
import csv

# Bij set_output_value zetten we een spanning over het circuit.
# Bij get_output_value return je de spaniong over het circuit.

with open('metingen.csv', 'w', newline='') as csvfile:
     writer = csv.writer(csvfile)
     writer.writerow(['U', 'I'])
     for a, b in zip(device.U_LED, device.I_LED):
        writer.writerow([a, b])

class DiodeExperiment():
    def __init__(self):
        from arduino_device import ArduinoVISADevice, list_devices
        port = "ASRL9::INSTR"
        self.device = ArduinoVISADevice(port=port)
    def scan(self):
        for value in range(0,1023):
            self.device.set_output_value(value)
            U_tot = self.device.get_output_value() 
            U_2 = self.device.get_input_value(channel = 2) 
            U_1 = int(U_tot) - int(U_2)
            self.device.U_LED.append(U_1)
            I = int(U_1) / 220
            self.device.I_LED.append(I)
        self.device.set_output_value(0)
        return self.device.U_LED, self.device.I_LED

model=DiodeExperiment()
data = model.scan()
U = data[0]
I = data[1]

plt.plot(U, I)
plt.show()