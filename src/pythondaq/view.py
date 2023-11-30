import matplotlib.pyplot as plt
import csv
from pythondaq.diode_experiment import DiodeExperiment


def view():
   """Plotting the voltage and current and putting them in a csv file
   """
   # I take the data out of the model
   model=DiodeExperiment(port="ASRL9::INSTR")
   data = model.scan(0, 1023, 1)

   std_I = data[3]
   gem_I = data[2]
   std_U = data[1]
   gem_U = data[0]

	# I plot the data
   plt.errorbar(gem_U, gem_I, yerr = std_I, xerr = std_U, fmt="o", ms=3)
   plt.xlabel("Spanning in Volt")
   plt.ylabel("Stroomsterkte in Ampere")


   # I store the data in a csv file
   with open('metingen.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['U', 'I'])
      for a, b in zip(data[0], data[1]):
         writer.writerow([a, b])
   return  plt.show()