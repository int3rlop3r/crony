from __future__ import print_function

import sys
import pwd
import os

def write_jobs(jobs, file=sys.stdout):
    """Write jobs to a file"""
    for job in jobs:
        print(job, file=file)

def get_username():
    return str(pwd.getpwuid(os.getuid()).pw_name)
