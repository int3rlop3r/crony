import click

from . import utils, parsers, views
from .crontab import Crontab

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

@click.group()
def crony():
    pass

@crony.command()
@click.option('--limit', default=0,
                        help="Number of crons to display, displays all by default")
@click.argument('host', default='localhost', 
                        callback=parsers.parse_hostname_callback, 
                        required=False)
def ls(limit, host):
    """List cron jobs on a remote or local system"""
    ct = Crontab(**host)
    cps = ct.list()
    jobs = parsers.parse_file(cps.stdout, limit)

    if not jobs:
        return
    
    # create the table and display it
    click.echo(views.horizontal_table(jobs))

@crony.command()
@click.option('--ids', default="0", callback=parsers.parse_range_callback,
                      help='IDs of jobs to be deleted.')
@click.argument('dst_host', default='localhost', 
                        callback=parsers.parse_hostname_callback, 
                        required=False)
def rm(ids, dst_host):
    """Delete cron jobs from a remote or local system"""
    confirm_msg = "Delete all jobs at: %s? (yes/no)" % (dst_host['hostname'],)

    # delete entire crontab
    if 0 in ids and (click.prompt(confirm_msg) == 'yes'):
        dst_ct = Crontab(**dst_host)
        dst_ps = dst_ct.remove()
        for out in dst_ps.stdout:
            click.echo(out)
        click.echo("Crontab deleted")
    else:
        if not click.prompt("Delete selected jobs? (yes/no)") == "yes":
            return # exit if not confirmed

        # delete selected jobs
        click.echo("Fetching remote jobs")
        dst_ct = Crontab(**dst_host)
        dst_ps = dst_ct.list()
        dst_jobs = parsers.parse_file(dst_ps.stdout)
        rm_jobs = dst_jobs.in_ids(ids)
        job_str = StringIO()

        for rm_job in rm_jobs:
            dst_jobs.remove(rm_job)

        utils.write_jobs(dst_jobs, job_str)
        rmt_ct = Crontab(**dst_host)

        # if there was only one job, delete the crontab
        click.echo("Applying changes")
        if len(dst_jobs):
            rmt_ps = rmt_ct.copy_new(job_str.getvalue())
        else:
            rmt_ps = rmt_ct.remove()

        for out in rmt_ps.stdout:
            click.echo(out)

        click.echo("Selected jobs deleted")

@crony.command()
@click.option('--ids', callback=parsers.parse_range_callback, help="IDs of crons to be deleted.")
@click.argument('src_host', nargs=1, callback=parsers.parse_hostname_callback)
@click.argument('dst_host', nargs=1, callback=parsers.parse_hostname_callback)
def cp(ids, src_host, dst_host):
    """Copy cron jobs across servers"""
    src_ct = Crontab(**src_host)
    src_ps = src_ct.list()
    src_jobs = parsers.parse_file(src_ps.stdout).in_ids(ids)
    job_str = StringIO()
    utils.write_jobs(src_jobs, job_str)

    dst_ct = Crontab(**dst_host)
    rmt_pd = dst_ct.append(job_str.getvalue())
    for out in rmt_pd.stdout:
        click.echo(out)

    click.echo("Done, copied: " + str(len(ids)))

def main():
    crony()

if __name__ == '__main__':
    main()

