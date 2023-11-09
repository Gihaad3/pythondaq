import pyvisa

class ArduinoVISADevice():
   
    def __init__(self, port):
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(
            "ASRL9::INSTR", read_termination="\r\n", write_termination="\n"\
        )

    def get_identification(self):
        return self.device.query("*IDN?")
        
    def set_output_value(self, value):
        self.device.query(f"OUT:CH0 {value}")

    def get_output_value(self):
        return self.device.query(f"MEAS:CH1?")

    def get_input_value(self, channel):
        return self.device.query(f"MEAS:CH{channel}?")


    def get_input_voltage(self, channel=2):
        V= 3.3/1023 * int(self.device.query(f"MEAS:CH{channel}?"))
        return V


def list_devices():
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()