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
@click.option('--ids', callback=utils.parse_range_callback,
                      help='IDs of crons to be deleted.')
def rm(ctx, ids):
    """Delete a crontabs from remote or local system"""
    click.echo("Delete all crons in the system in range: %s!" % ids)

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
