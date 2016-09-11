
class Jobs:

    def __init__(self, jobs=[]):
        self._index = 0
        self._jobs = jobs

    def __len__(self):
        return len(self._jobs)

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index > len(self._jobs):
            raise StopIteration
        return self.get(self._index)

    next = __next__

    def add(self, job):
        """Adds a job to the list"""
        if not isinstance(job, Job):
            raise AttributeError("expected {} but got {}".format(Job, type(job)))

        self._jobs.append(job)

    def get(self, index):
        """Gets a job by index"""
        return self._jobs[index - 1]

    def merge(self, jobs):
        if not isinstance(jobs, Jobs):
            raise TypeError("Jobs must be of type: 'Jobs'")

        # merge jobs
        self._jobs = self._jobs + jobs._jobs
        return self

    def in_ids(self, job_ids):
        """Get jobs that have the ids specified"""
        j = []
        for job_id in job_ids:
            j.append(self.get(job_id))
        
        return Jobs(j)

    def all(self):
        """Returns all jobs as a list"""
        return self._jobs

    def remove(self, job):
        """Removes a job from the list"""
        self._jobs.remove(job)

    def clear_all(self):
        self._jobs = []

MINUTE = 0
HOUR = 1
DAY_OF_MONTH = 2
MONTH = 3
DAY_OF_WEEK = 4

class Job(object):
    
    def __init__(self, job_line=""):
        # Set default values for all job fields
        self.command = ''
        self.comments = ''
        self.log_file = ''
        self.error_log_file = ''
        self._exp_fields = []

        if job_line:
            self.line = job_line

    def __str__(self):
        return self.line

    @property
    def minute(self):
        return self._exp_fields[MINUTE]

    @property
    def hour(self):
        return self._exp_fields[HOUR]

    @property
    def day_of_month(self):
        return self._exp_fields[DAY_OF_MONTH]

    @property
    def month(self):
        return self._exp_fields[MONTH]

    @property
    def day_of_week(self):
        return self._exp_fields[DAY_OF_WEEK]

    @property
    def expression(self):
        return "{0} {1} {2} {3} {4}".format(
                        self.minute,
                        self.hour,
                        self.day_of_month,
                        self.month,
                        self.day_of_week)

    @expression.setter
    def expression(self, expression):
        """Set the crontab expression"""
        if type(expression) is list:
            self._exp_fields = expression
        else:
            self._exp_fields = expression.split()

    @property
    def line(self):
        """Creates a crontab string from all params passed"""
        cron_string = self.expression + ' ' + self.command

        if self.log_file:
            cron_string += ' >> ' + self.log_file

        if self.error_log_file:
            cron_string += ' 2>> ' + self.error_log_file

        if self.comments:
            cron_string += ' # ' + self.comments

        return cron_string

    @line.setter
    def line(self, job_line):
        """Parse a crontab line"""
        crontab_pieces = job_line.split()

        # set the expression part
        self.expression = crontab_pieces[:5]

        # set the latter part of the job
        latter_part = ' '.join(crontab_pieces[5:])

        # extract the comment part
        comment_start = latter_part.find('#')
        if comment_start != -1:
            comments_part = latter_part[comment_start:].strip()
            self.comments = comments_part.lstrip('#').strip()
            latter_part = latter_part[:comment_start].strip()

        # extract the err log part
        err_log_start = latter_part.find('2>>')
        if err_log_start != -1:
            err_log_part = latter_part[err_log_start:].strip()
            self.error_log_file = err_log_part.lstrip('2>>').strip()
            latter_part = latter_part[:err_log_start].strip()

        err_log_start = latter_part.find('2>')
        if err_log_start != -1:
            err_log_part = latter_part[err_log_start:].strip()
            self.error_log_file = err_log_part.lstrip('2>').strip()
            latter_part = latter_part[:err_log_start].strip()

        # extract the log part
        log_start = latter_part.find('>>')
        if log_start != -1:
            log_part = latter_part[log_start:].strip()
            self.log_file = log_part.lstrip('>>').strip()
            latter_part = latter_part[:log_start].strip()

        log_start = latter_part.find('>')
        if log_start != -1:
            log_part = latter_part[log_start:].strip()
            self.log_file = log_part.lstrip('>').strip()
            latter_part = latter_part[:log_start].strip()

        # finally set the command to run
        self.command = latter_part

