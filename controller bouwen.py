import pyvisa
import matplotlib.pyplot as plt
import csv
from arduino_device import ArduinoVISADevice, list_devices

port = "ASRL9::INSTR"
device = ArduinoVISADevice(port=port)

# Bij set_output_value zetten we een spanning over het circuit.
# Bij get_output_value return je de spaniong over het circuit.

for x in range (0, 1024):
    device.set_output_value(x)
    U_tot = device.get_output_value() 
    U_2 = device.get_input_value(channel = 2) 
    U_1 = int(U_tot) - int(U_2)
    device.U_LED.append(U_1)
    I = int(U_1) / 220
    device.I_LED.append(I)
device.set_output_value(0)

plt.plot(device.U_LED, device.I_LED)
plt.show()

with open('metingen.csv', 'w', newline='') as csvfile:
     writer = csv.writer(csvfile)
     writer.writerow(['U', 'I'])
     for a, b in zip(device.U_LED, device.I_LED):
        writer.writerow([a, b])