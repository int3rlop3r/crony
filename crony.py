import click
import utils
import parser
import views
from crontab import Crontab

@click.group()
def crony():
    pass

@click.command()
@click.option('--limit', default=10,
                      help='Number of crons to display, displays 10 by default')
@click.option('--host', default=None, help='List crons for <host>')
def ls(limit, host):
    """List crontabs on a remote or local system"""
    ct = Crontab(host=host)
    cps = ct.list()
    jobs = parser.parse_file(cps.stdout, limit)

    if not jobs:
        click.echo("No crontabs set")
        return
    
    # create the table and display it
    click.echo(views.horizontal_table(jobs))

@click.command()
@click.option('--ids', callback=utils.parse_range_callback,
                      help='IDs of crons to be deleted.')
def rm(ids):
    """Delete a crontabs from remote or local system"""
    click.echo("Delete all crons in the system in range: %s!" % ids)

@click.command()
@click.option('--ids', callback=utils.parse_range_callback,
                      help='IDs of crons to be deleted.')
@click.argument('src_host', nargs=1)
@click.argument('dst_host', nargs=1)
def cp(ids, src, dst):
    """Copy crontabs across servers"""
    click.echo("Delete all crons in the system in range: %s!" % ids)

if __name__ == '__main__':
    crony.add_command(ls)
    crony.add_command(rm)
    crony.add_command(cp)
    crony()
