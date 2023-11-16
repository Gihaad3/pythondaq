import pyvisa

# Deze class stuurt opdrachten naar de arduino
class ArduinoVISADevice():
   
    # Deze method opent de arduino
    def __init__(self, port):
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(
            port, read_termination="\r\n", write_termination="\n"\
        )

    #Deze method geeft de inditentificatie string terug
    def get_identification(self):
        return self.device.query("*IDN?")
        
     #Deze method stuurt een spanning over het circuit
    def set_output_value(self, value):
        self.device.query(f"OUT:CH0 {value}")

    # Deze method meet de spanning over het hele circuit
    def get_output_value(self):
        return self.device.query(f"MEAS:CH0?")

    # Deze method meet de spanning over een bepaald kanaal
    def get_input_value(self, channel):
        return self.device.query(f"MEAS:CH{channel}?")

    # Deze method zet de spanning van ADC naar Volt om
    def get_input_voltage(self, channel=2):
        V= 3.3/1023 * int(self.device.query(f"MEAS:CH{channel}?"))
        return V

# deze functie geeft alle mogelijke lijsten terug
def list_devices():
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()