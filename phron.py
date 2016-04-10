import click
import utils

@click.group()
def phron():
    pass

@click.command()
@click.option('--range', default=10, help='Number of crons to display')
def ls():
    click.echo("All crons in the system!")

@click.command()
@click.option('--ids', callback=utils.parse_range_callback, help='ids of crons to be deleted.')
def rm(ids):
    click.echo("Delete all crons in the system in range: %s!" % ids)

if __name__ == '__main__':
    phron.add_command(ls)
    phron.add_command(rm)
    phron()
