import matplotlib.pyplot as plt
import csv
from pythondaq.diode_experiment import DiodeExperiment

# Deze functie geeft door dat het experiment 
# moet worden uitgevoerd
def view():
   # Ik neem de data uit de model
   model=DiodeExperiment()
   data = model.scan(0, 1023)
   U = data[0]
   I = data[1]
   error = model.std_calc(0, 1023)

	#Ik plot alles
   plt.scatter(U, I)
   plt.errorbar(U, error[0], yerr = error[1])
   plt.xlabel("Spanning in Volt")
   plt.ylabel("Stroomsterkte in Ampere")

   plt.show()

   #Ik sla de data op in een csv bestand
   with open('metingen.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['U', 'I'])
      for a, b in zip(data[0], data[1]):
         writer.writerow([a, b])
   return  plt.show()