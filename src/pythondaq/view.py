import matplotlib.pyplot as plt
import csv
from pythondaq.diode_experiment import DiodeExperiment


def view():
   """Plotting the voltage and current and putting them in a csv file
   """
   # I take the data out of the model
   model=DiodeExperiment()
   data = model.scan(0, 1023, 10)

   std_I = data[0]
   gem_I = data[1]
   std_U = data[2]
   gem_U = data[3]

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