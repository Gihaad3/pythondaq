import pyvisa


class ArduinoVISADevice():
    """This class sends assignments the the arduino
    """

    def __init__(self, port):
        """This method opens the device
        """
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(
            port, read_termination="\r\n", write_termination="\n"
        )

    
    def get_identification(self):
        """This method gives the identification string of the device

        Returns:
            string: the identification string
        """
        return self.device.query("*IDN?")
    
    
    def set_output_value(self, value):
        """This method aplies a voltage in units of ADC(from 0-1023)
        """
        
        self.device.query(f"OUT:CH0 {value}")

    
    def get_output_value(self):
        """This method measers the voltage in ADC over the enitre circuit

        Returns:
            integer: a value from 0-1023 in ADC
        """
        return self.device.query(f"MEAS:CH0?")

    
    def get_input_value(self, channel):
        """This method measures the voltage in units ADC over a given channel

        Returns:
            integer: a value from 0-1023 in ADC
        """

        return self.device.query(f"MEAS:CH{channel}?")

    def get_input_voltage(self, channel):
        """This method measures the voltage in units Volt over a given channel

        Returns:
            integer: a value from 0-3.3 in Volts
        """
        V= 3.3/1023 * int(self.device.query(f"MEAS:CH{channel}?"))
        return V


def list_devices():
    """This function gives a the availebele lists

    Returns:
        integer: individual lists
    """
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()

def identification(port):
    rm = pyvisa.ResourceManager("@py")
    device = rm.open_resource(
        port, read_termination="\r\n", write_termination="\n"
    )
    return device.query("*IDN?")