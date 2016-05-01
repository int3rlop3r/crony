import click
import utils
import parser
import views
import io
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
@click.option('--ids', callback=utils.parse_range_callback, help='IDs of crons to be deleted.')
@click.argument('src_host', nargs=1)
@click.argument('dst_host', nargs=1)
def cp(ids, src_host, dst_host):
    """Copy crontabs across servers"""
    src_ct = Crontab(host=src_host)
    src_ps = src_ct.list()
    src_jobs = parser.parse_file(src_ps.stdout).in_ids(ids)

    dst_ct = Crontab(host=dst_host)
    dst_ps = dst_ct.list()
    dst_jobs = parser.parse_file(dst_ps.stdout).in_ids(ids)
    dst_jobs.merge(src_jobs)
    job_str = io.StringIO()
    utils.print_jobs(dst_jobs, job_str)
    click.echo("Uploading new crons to: " + dst_host)

    rmt_ct = Crontab(host=dst_host)
    rmt_ps = rmt_ct.install(jobs)
    for out in rmt_ps.stdout:
        click.echo(out)

if __name__ == '__main__':
    crony.add_command(ls)
    crony.add_command(rm)
    crony.add_command(cp)
    crony()
