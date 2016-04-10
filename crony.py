import click
import utils
from crontab import Crontab
from prettytable import PrettyTable

@click.group()
def crony():
    pass

@click.command()
@click.option('--limit', default=10, help='Number of crons to display, displays 10 by default')
def ls(limit):
    ct = Crontab()
    cps = ct.list()
    jobs = utils.parse_file(cps.stdout, limit)
    t = PrettyTable(("ID", "Command", "Expression", "Log File", "Error Log"))
    id_counter = 1
    for job in jobs:
        t.add_row((id_counter, 
                   job.command, 
                   job.expression, 
                   job.log_file,
                   job.error_log_file))
        id_counter += 1
    click.echo(t)

@click.command()
@click.option('--ids', callback=utils.parse_range_callback, help='ids of crons to be deleted.')
def rm(ids):
    click.echo("Delete all crons in the system in range: %s!" % ids)

if __name__ == '__main__':
    crony.add_command(ls)
    crony.add_command(rm)
    crony()
