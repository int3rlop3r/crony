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
@click.argument('hostname', default=None, required=False)
def ls(limit, hostname):
    """List crontabs on a remote or local system"""
    ct = Crontab(remote_server=hostname)
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
@click.argument('src_hostname', nargs=1)
@click.argument('dst_hostname', nargs=1)
def cp(ids, src_hostname, dst_hostname):
    """Copy crontabs across servers"""
    src_ct = Crontab(remote_server=src_hostname)
    src_ps = src_ct.list()
    src_jobs = parser.parse_file(src_ps.stdout).in_ids(ids)
    job_str = io.StringIO()
    utils.write_jobs(src_jobs, job_str)

    dst_ct = Crontab(remote_server=dst_hostname)
    rmt_pd = dst_ct.append(job_str.getvalue())
    for out in rmt_pd.stdout:
        click.echo(out)

    # click.echo("Jobs: {}".format(job_str.getvalue()))
    # dst_ct = Crontab(remote_server=dst_hostname)
    # dst_ps = dst_ct.list()
    # dst_jobs = parser.parse_file(dst_ps.stdout)
    # dst_jobs.merge(src_jobs)
    # job_str = io.StringIO()
    # utils.write_jobs(dst_jobs, job_str)
    # click.echo("Copying new crons to: " + dst_hostname)

    # rmt_ct = Crontab(remote_server=dst_hostname)
    # rmt_ps = rmt_ct.install(jobs)
    # for out in rmt_ps.stdout:
        # click.echo(out)

if __name__ == '__main__':
    crony.add_command(ls)
    crony.add_command(rm)
    crony.add_command(cp)
    crony()
