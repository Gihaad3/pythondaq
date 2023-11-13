import matplotlib.pyplot as plt
import csv
from diode_experiment import DiodeExperiment

model=DiodeExperiment()
data = model.scan(100, 1000)
U = data[0]
I = data[1]

plt.scatter(U, I)
plt.show()

with open('metingen.csv', 'w', newline='') as csvfile:
     writer = csv.writer(csvfile)
     writer.writerow(['U', 'I'])
     for a, b in zip(data[0], data[1]):
        writer.writerow([a, b])