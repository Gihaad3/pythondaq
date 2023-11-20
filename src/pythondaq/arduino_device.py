import pyvisa

"""This class sends assignments the the arduino
"""
class ArduinoVISADevice():

    """This method opens the device
    """
    def __init__(self, port):
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(
            port, read_termination="\r\n", write_termination="\n"\
        )

    """This method gives the identification string of the device

    Returns:
        string: the identification string
    """
    def get_identification(self):
        return self.device.query("*IDN?")
    
    """This method aplies a voltage in units of ADC(from 0-1023)
    """
    def set_output_value(self, value):
        self.device.query(f"OUT:CH0 {value}")

    """This method measers the voltage in ADC over the enitre circuit

    Returns:
        integer: a value from 0-1023 in ADC
    """
    def get_output_value(self):
        return self.device.query(f"MEAS:CH0?")

    """This method measures the voltage in units ADC over a given channel

    Returns:
        integer: a value from 0-1023 in ADC
    """
    def get_input_value(self, channel):
        return self.device.query(f"MEAS:CH{channel}?")

    """This method measures the voltage in units Volt over a given channel

    Returns:
        integer: a value from 0-3.3 in Volts
    """
    def get_input_voltage(self, channel=2):
        V= 3.3/1023 * int(self.device.query(f"MEAS:CH{channel}?"))
        return V

"""This function gives a the availebele lists

Returns:
    integer: individual lists
"""
def list_devices():
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()