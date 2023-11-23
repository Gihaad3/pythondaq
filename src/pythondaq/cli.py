import click
from pythondaq.arduino_device import ArduinoVISADevice, list_devices, identification
from pythondaq.diode_experiment import DiodeExperiment
import csv
import matplotlib.pyplot as plt

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
@click.option(
    "-r",
    "--repeats",
    default=1,
    help="repeats the experiment a number of times.",
    show_default = True,
)
@click.option(
    "-p",
    "--port",
    help="gives the ability to choose a device from the command list",
    show_default=True
)
@click.option(
    "-g",
    "--graph/--no-graph",
    default=False,
    help="this plots the data in a scattr plot",
)

def scan(min, max, output, repeats, port, graph):
    if port is None:
        print("Error: No port given")
    else:
        model = DiodeExperiment(port=port)
        data = model.scan(min, max, N=repeats)
        std_I = data[0]
        gem_I = data[1]
        std_U = data[2]
        gem_U = data[3]
        measurments = []
        for volt in range(min, max):
            measurments.append([data[3][volt], data[1][volt]])
        
        if output is not None:       
            with open(f'{output}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['U', 'I'])
                for a, b in zip(data[3], data[1]):
                    writer.writerow([a, b])
    
        if graph is not None:
            plt.errorbar(gem_U, gem_I, yerr = std_I, xerr = std_U, fmt="o", ms=1)
            plt.xlabel("Spanning in Volt")
            plt.ylabel("Stroomsterkte in Ampere")
            return print(measurments), plt.show()
        else:
            return print(measurments)


@cmd_group.command()
@click.option(
    "-p",
    "--port",
    help="gives the ability to choose a device from the command list",
    show_default=True)
def info(port):
    if port is None:
        print("Error: No port given")
    else:
        return print(identification(port))