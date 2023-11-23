import click
from pythondaq.arduino_device import ArduinoVISADevice, list_devices
from pythondaq.diode_experiment import DiodeExperiment

@click.group()
def cmd_group():
    pass

# @cmd_group.command()
# @click.option(

#     default=1,
#     help="print",
#     show_default=True,
# )
# def list():
#     return print("hallo")




@cmd_group.command()
@click.option(
    "--min",
    default=0,
    help="this gives the minimum voltage over the circuit.",
    show_default=True
)

@click.option(
    "--max",
    default=1023,
    help="this gives the maximum voltage over the circuit.",
    show_default=True
)

def scan(min, max):
    model = DiodeExperiment()
    data = model.scan(min, max, N=1)
    measurments = []
    for volt in range(min, max):
        measurments.append([data[3][volt], data[1][volt]])
    return print(measurments)