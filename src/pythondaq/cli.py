import click
from pythondaq.arduino_device import ArduinoVISADevice, list_devices
from pythondaq.diode_experiment import DiodeExperiment
import csv

@click.group()
def cmd_group():
    pass

@cmd_group.command('list')
def list():
    return print(list_devices())



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
@click.option(
    "--output",
    help="this outputs the data in a csv ddocument.",
    show_default = True,
)
def scan(min, max, output):
    model = DiodeExperiment()
    data = model.scan(min, max, N=1)
    measurments = []
    for volt in range(min, max):
        measurments.append([data[3][volt], data[1][volt]])
    
    if output is not None:       
        with open(f'{output}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['U', 'I'])
            for a, b in zip(data[3], data[1]):
                writer.writerow([a, b])
       
    return print(measurments)