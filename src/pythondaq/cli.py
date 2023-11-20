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

    default=1,
    help="print",
    show_default=True,
)
def scan():
    return print("nee")
