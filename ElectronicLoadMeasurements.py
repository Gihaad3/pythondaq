class ElectronicLoadMeasurements:
    def __init__(self):
        self.R = []
        self.U = []
        self.I = []
        self.P = []
    
    def add_measurement(self, R, U):
      self.R.append(R)
      self.U.append(U)

    def get_loads(self):
        return self.R

    def get_voltages(self):
        return self.U

    def get_currents(self):
        self.I.clear()
        for x in range(len(self.R)):
            I = self.U[x] / self.R[x]
            self.I.append(I)
        return  self.I
    
    def get_powers(self):
        self.P.clear()
        for x in range(len(self.R)):
            P = (self.U[x])**2 / self.R[x]
            self.P.append(P)
        return self.P

    def clear(self):
        self.R.clear()
        self.U.clear()
        self.P.clear()
        self.I.clear()



measurements = ElectronicLoadMeasurements()

measurements.add_measurement(R=10, U=.5)
measurements.add_measurement(R=20, U=1.5)

R = measurements.get_loads()
# R=[10, 20]
U = measurements.get_voltages()
# U=[0.5, 1.5]
P = measurements.get_powers()
# P=[0.025, 0.1125]
I = measurements.get_currents()
# I=[0.05, 0.075]

print(R)
print(U)
print(P)
print(I)

print(R)
print(P)
print(U)
print(I)


measurements.clear()
print(R)
print(U)
print(P)
print(I)


