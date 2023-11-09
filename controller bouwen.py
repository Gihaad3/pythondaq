import matplotlib.pyplot as plt
import csv
from diode_experiment import DiodeExperiment
# Bij set_output_value zetten we een spanning over het circuit.
# Bij get_output_value return je de spaniong over het circuit.

with open('metingen.csv', 'w', newline='') as csvfile:
     writer = csv.writer(csvfile)
     writer.writerow(['U', 'I'])
     for a, b in zip(device.U_LED, device.I_LED):
        writer.writerow([a, b])

model=DiodeExperiment()
data = model.scan(100, 1000)
U = data[0]
I = data[1]

plt.plot(U, I)
plt.show()