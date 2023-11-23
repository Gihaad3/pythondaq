import click

@click.group()
def cmd_group():
    pass

@cmd_group.command()
@click.option(

    default=1,
    help="print",
    show_default=True,
)
def list():
    return print("hallo")




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

def scan():
    return print("nee")
