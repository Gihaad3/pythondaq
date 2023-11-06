import pyvisa

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()
device = rm.open_resource(
    "ASRL9::INSTR", read_termination="\r\n", write_termination="\n"
)