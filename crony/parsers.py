import os
import click
from . import utils
from .builder import Job, Jobs

def parse_range_callback(ctx, param, value):
    """Callback function that parses the range entered
    from the commandline
    """
    try:
        if not value:
            raise ValueError("ids required")
        return parse_range(value)
    except (ValueError, TypeError) as ve:
        raise click.BadParameter(str(ve))

def parse_hostname_callback(ctx, param, value):
    """Callback function that parses the hostname entered
    from the commandline
    """
    try:
        if not value:
            raise ValueError("hostname required")
        return parse_hostname(value)
    except (ValueError, TypeError) as ve:
        raise click.BadParameter(str(ve))

def parse_range(value):
    """
    Parses the range entered as string and returns a set
    eg:
        The string 1,2,3,4 would be { 1, 2, 3, 4 }
        1-5 would be { 1, 2, 3, 4, 5 }
        1,2,4-6 would be {1, 2, 4, 5, 6}
    """
    cronids = set()
    ids = value.split(',')
    for cron_id in ids:
        if '-' in cron_id:
            cron_id_pcs = cron_id.split('-')

            # this has to be 2, eg: 1-5, not 1-5-8, etc.
            if len(cron_id_pcs) != 2:
                raise ValueError("Invalid range: %s" % cron_id)

            start_idx = int(cron_id_pcs[0])
            end_idx = int(cron_id_pcs[1]) + 1

            if not 0 < start_idx < end_idx:
                raise ValueError("Invalid range: %s" % cron_id)

            for cid in range(start_idx, end_idx):
                cronids.add(int(cid))
        else:
            cronids.add(int(cron_id))
    return cronids

def parse_file(cronfd=None, cronfile=None, num_lines=0):
    """Parses a cron file and returns a Job object"""
    if cronfile:
        cfd = open(cronfile)
    elif cronfd:
        cfd = cronfd
    else:
        raise ValueError("No stream or file path mentioned")

    joblist = []
    line_counter = 1

    for line in cfd:
        if hasattr(line, 'decode'):
            cronline = line.decode("utf-8").strip()
        else:
            cronline = line.strip()

        # ignore comments and blank lines
        if not cronline or cronline[0] == '#':
            continue

        # add jobs to list
        job = Job(cronline)
        joblist.append(job)

        if num_lines > 0 and line_counter >= num_lines:
            break
        else:
            line_counter += 1

    cfd.close()
    return Jobs(joblist)

def parse_hostname(hostname):
    """Parses an ssh hostname into different parts (host, 
    username, port)
    """
    details = {
        'port': '22',
    }

    # extract username if it exists in the hostname
    username_start = hostname.find('@')
    if username_start != -1:
        details['username'] = hostname[:username_start].strip()
        hostname = hostname[username_start + 1:]

    # extract the port no. if it exists in the hostname
    port_start = hostname.find(':')
    if port_start != -1:
        port_part = hostname[port_start:]
        details['port'] = port_part.lstrip(':').strip()
        hostname = hostname[:port_start]

    # what ever will be left will be the hostname
    details['hostname'] = hostname

    return details

