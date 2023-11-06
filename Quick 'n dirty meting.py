import pyvisa

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()
device = rm.open_resource(
    "ASRL9::INSTR", read_termination="\r\n", write_termination="\n"
)

U_LED = []
for x in range (0, 1024):
    device.query(f"OUT:CH0 {x}")
    U_tot = device.query("MEAS:CH1?") 
    U_2 = device.query("MEAS:CH2?") 
    U_1 = U_tot - U_2
    U_LED.append(U_1)

