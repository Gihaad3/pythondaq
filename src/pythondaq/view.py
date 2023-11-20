import matplotlib.pyplot as plt
import csv
from pythondaq.diode_experiment import DiodeExperiment

# Deze functie geeft door dat het experiment 
# moet worden uitgevoerd
def view():
   # Ik neem de data uit de model
   model=DiodeExperiment()
   data = model.scan(0, 1023, 10)

   std_I = data[0]
   gem_I = data[1]
   std_U = data[2]
   gem_U = data[3]

	#Ik plot alles
   plt.errorbar(gem_U, gem_I, yerr = std_I, xerr = std_U, fmt="o", ms=3)
   plt.xlabel("Spanning in Volt")
   plt.ylabel("Stroomsterkte in Ampere")


   #Ik sla de data op in een csv bestand
   with open('metingen.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['U', 'I'])
      for a, b in zip(data[0], data[1]):
         writer.writerow([a, b])
   return  plt.show()