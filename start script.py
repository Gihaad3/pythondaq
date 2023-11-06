import pyvisa

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()
device = rm.open_resource(
    "ASRL9::INSTR", read_termination="\r\n", write_termination="\n"
)


for x in range(0, 1024):
     device.query(f"OUT:CH0 {x}")
