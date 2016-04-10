import os
from .builder import Job, Jobs

class FileParser:
    
    def __init__(self, cronfile=None):
        if type(cronfile) == file:
            self.fd = cronfile
            self.isfile = False
        else:
            self.set_file(cronfile)
            self.isfile = True

    def set_file(self, cronfile):
        """Sets the file to be parsed"""
        open(cronfile).close()
        self.cronfile = cronfile

    def get_jobs(self):
        """Runs the parser on the set file and
        returns a list of jobs"""
        self.jobs = Jobs()

        if isfile:
            cfd = open(self.cronfile)

        for line in cfd:
            cronline = line.strip()
            # ignore comments and blank lines
            if not cronline or cronline[0] == '#':
                continue

            # add jobs to list
            print('Adding: ' + cronline)
            job = Job(cronline)
            self.jobs.add(job)

        return self.jobs.all()

