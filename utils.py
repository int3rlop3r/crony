import sys
import click
import parser

def parse_range_callback(ctx, param, value):
    """Callback function that parses the range entered
    from the commandline"""
    try:
        if not value:
            return set()
        return parser.parse_range(value)
    except (ValueError, TypeError) as ve:
        raise click.BadParameter(str(ve))

def print_jobs(jobs, file=sys.stdout):
    """Write jobs to a file"""
    for job in jobs:
        print(job, file=file)
