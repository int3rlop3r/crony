import click
import utils
import parser
import views
import io
from crontab import Crontab

@click.group()
@click.option('--port', default=22, help="Port number")
@click.pass_context
def crony(ctx, port):
    ctx.obj['ssh_port'] = port

@crony.command()
@click.option('--limit', default=10,
                      help='Number of crons to display, displays 10 by default')
@click.argument('hostname', default=None, required=False)
@click.pass_context
def ls(ctx, limit, hostname):
    """List crontabs on a remote or local system"""
    ct = Crontab(remote_server=hostname, port=ctx.obj['ssh_port'])
    cps = ct.list()
    jobs = parser.parse_file(cps.stdout, limit)

    if not jobs:
        return
    
    # create the table and display it
    click.echo(views.horizontal_table(jobs))

@crony.command()
@click.pass_context
@click.option('--ids', default="0", callback=utils.parse_range_callback,
                      help='IDs of jobs to be deleted.')
@click.argument('dst_hostname', default=None, required=False)
def rm(ctx, ids, dst_hostname):
    """Delete crontabs from a remote or local system"""
    # dst_ct = Crontab(remote_server=dst_hostname, port=ctx.obj['ssh_port'])
    hostname = dst_hostname if dst_hostname else 'localhost'
    confirm_msg = "Deleting all jobs at: %s? (yes/no)" % (hostname,)

    # delete entire crontab
    if 0 in ids and (click.prompt(confirm_msg) == 'yes'):
        dst_ct = Crontab(remote_server=dst_hostname, port=ctx.obj['ssh_port'])
        dst_ps = dst_ct.remove()
        for out in dst_ps.stdout:
            click.echo(out)
        click.echo("Crontab deleted")
    else:
        if not click.prompt("Delete selected jobs? (yes/no)") == "yes":
            return # exit if not confirmed

        # delete selected jobs
        dst_ct = Crontab(remote_server=hostname, port=ctx.obj['ssh_port'])
        dst_ps = dst_ct.list()
        dst_jobs = parser.parse_file(dst_ps.stdout)
        job_str = io.StringIO()

        for cid in ids:
            dst_jobs.remove(cid)

        utils.write_jobs(dst_jobs, job_str)
        rmt_ct = Crontab(remote_server=dst_hostname, port=ctx.obj['ssh_port'])

        # if there was only one jobs, delete the crontab
        if len(dst_jobs):
            rmt_ps = rmt_ct.copy_new(job_str.getvalue())
        else:
            rmt_ps = rmt_ct.remove()

        for out in rmt_ps.stdout:
            click.echo(out)

        click.echo("Selected jobs deleted")

@crony.command()
@click.pass_context
@click.option('--ids', callback=utils.parse_range_callback, help='IDs of crons to be deleted.')
@click.option('--dst-port', default=22, help='Destination port number.')
@click.argument('src_hostname', nargs=1)
@click.argument('dst_hostname', nargs=1)
def cp(ctx, ids, dst_port, src_hostname, dst_hostname):
    """Copy crontabs across servers"""
    src_ct = Crontab(remote_server=src_hostname, port=ctx.obj['ssh_port'])
    src_ps = src_ct.list()
    src_jobs = parser.parse_file(src_ps.stdout).in_ids(ids)
    job_str = io.StringIO()
    utils.write_jobs(src_jobs, job_str)

    dst_ct = Crontab(remote_server=dst_hostname, port=dst_port)
    rmt_pd = dst_ct.append(job_str.getvalue())
    for out in rmt_pd.stdout:
        click.echo(out)

    click.echo("Done, copied: " + str(len(ids)))

if __name__ == '__main__':
    crony(obj={})
