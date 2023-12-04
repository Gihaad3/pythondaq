import click
from pythondaq.diode_experiment import DiodeExperiment, list_devices, identification
import csv
import matplotlib.pyplot as plt
import numpy as np

@click.group()
def cmd_group():
    """I define the name of a command group.
    """    
    pass

@cmd_group.command('list')
def list():
    """I print all the availeble devices.

    Returns:
        	string: a list of devices
    """    
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
    default=3.3,
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
    """This is a command that measures the voltage over and the current trough a device.

    Args:
        min (int): the minimal voltage
        max (int): the maximum voltage
        output (string ): this eports the data in a csv document
        repeats (int): this gives the number of times the experiment is repeated
        port (string): thestring of the wanted device
        graph : this puts the data in a graph

    Returns:
        list: the voltage and current is printed in a list
    """    
    # the condition that the port name is given must be met
    if port is None:
        print("Error: No port given")
    else:
        # I run the experiment
        model = DiodeExperiment(port=port)
        data = model.scan(min, max, N=repeats)
        gem_U = data[0]
        std_U = data[1]
        gem_I = data[2]
        std_I = data[3]

        # I put the volt and ampere in one list of lists
        measurments = []

        
        # if a name is given than the data is exported as acsv file
        if output is not None:       
            with open(f'{output}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['U', 'std_U', 'I', 'std_I'])
                for a, b in zip(gem_U, std_U, gem_I, std_I):
                    writer.writerow([a, b])
    
        # If wanted the data is plotted
        if graph is not None:
            plt.errorbar(gem_U, gem_I, yerr = std_I, xerr = std_U, fmt="o", ms=1)
            plt.xlabel("Spanning in Volt")
            plt.ylabel("Stroomsterkte in Ampere")
            return plt.show()
        else:
            for a, b, c, d in zip(gem_U, std_U, gem_I, std_I):
                print([a,b,c,d])

@cmd_group.command()
@click.option(
    "-p",
    "--port",
    help="gives the ability to choose a device from the command list",
    show_default=True)
def info(port):
    """Gives the identification string if wanted

    Args:
        port (string): the identification string

    Returns:
        string: the identification string
    """    
    if port is None:
        print("Error: No port given")
    else:
        return print(identification(port))