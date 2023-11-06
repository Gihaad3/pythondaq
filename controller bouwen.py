import pyvisa
import matplotlib.pyplot as plt
import csv

class ArduinoVISADevice:
   
    def __init__(self):
        port = "ASRL3::INSTR"
        device = ArduinoVISADevice(port=port)

    def identificatiestring(self):
        print(device.get_identification())

    def setvalue(self, value):
        device.set_output_value(value=512)

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()
device = rm.open_resource(
    "ASRL9::INSTR", read_termination="\r\n", write_termination="\n"
)

U_LED = []
I_LED = []
for x in range (0, 1024):
    device.query(f"OUT:CH0 {x}")
    U_tot = device.query("MEAS:CH1?") 
    U_2 = device.query("MEAS:CH2?") 
    U_1 = int(U_tot) - int(U_2)
    U_LED.append(U_1)
    I = int(U_1) / 220
    I_LED.append(I)
device.query("OUT:CH0 0")

plt.plot(U_LED, I_LED)
plt.show()

with open('metingen.csv', 'w', newline='') as csvfile:
     writer = csv.writer(csvfile)
     writer.writerow(['U', 'I'])
     for a, b in zip(U_LED, I_LED):
        writer.writerow([a, b])