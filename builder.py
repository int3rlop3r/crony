import expvalidator

class Jobs:

    def __init__(self):
        self._index = 0
        self._jobs = []

    def __len__(self):
        return len(self._jobs)

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index > len(self._jobs):
            raise StopIteration
        return self.get(self._index)

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
        _jobs = Jobs()
        for job_id in job_ids:
            _job = self.get(job_id)
            _jobs.add(_job)
        
        return _jobs

    def all(self):
        """Returns all jobs as a list"""
        return self._jobs

    def remove(self, job):
        """Removes a job from the list
        If job is an int it will remove by index
        If job is an instance it will remove by instance
        """
        if isinstance(job, Job):
            self._jobs.remove(job)
        else:
            self._jobs.remove(self._jobs[job - 1])

    def clear_all(self):
        self._jobs = []

class Job:
    
    def __init__(self, crontab_line=""):
        # Set default values for all job fields
        self.command = ''
        self.comments = ''
        self.log_file = ''
        self.error_log_file = ''

        self.crontab_line = crontab_line
        if crontab_line:
            self.parse_line(crontab_line)

    def __str__(self):
        return self.render()

    def _set_cron_fields(self, fields):
        """Assign each part of the expression to a field"""
        self.minute = fields[0]
        self.hour = fields[1]
        self.day_of_month = fields[2]
        self.month = fields[3]
        self.day_of_week = fields[4]

    def set_expression(self, expression):
        """Set the crontab expression"""

        if isinstance(expression, str):
            expression_pieces = expression.split()
            self.expression = expression
        else:
            expression_pieces = expression
            self.expression = " ".join(expression)

        try:
            expvalidator.validate(expression_pieces)
            self._set_cron_fields(expression_pieces)
        except AttributeError:
            # only care about valid expressions
            # ignore invalid ones as they could
            # be an ssh banner.
            pass

    def set_command(self, command):
        """Set the command part"""
        self.command = command

    def set_log_file(self, log_file):
        """Set the path to the log file"""
        self.log_file = log_file

    def set_error_log_file(self, err_log_file):
        """Set the path to the error log file"""
        self.error_log_file = err_log_file

    def set_comments(self, comments):
        """Add comments"""
        self.comments = comments

    def parse_line(self, crontab_line):
        """Parse a crontab line"""
        crontab_pieces = crontab_line.split()

        # set the expression part
        self.set_expression(crontab_pieces[:5])

        # set the latter part of the job
        latter_part = ' '.join(crontab_pieces[5:])

        # extract the comment part
        comment_start = latter_part.find('#')
        if comment_start != -1:
            comments_part = latter_part[comment_start:].strip()
            self.set_comments(comments_part.lstrip('#').strip())
            latter_part = latter_part[:comment_start].strip()

        # extract the err log part
        err_log_start = latter_part.find('2>')
        if err_log_start != -1:
            err_log_part = latter_part[err_log_start:].strip()
            self.set_error_log_file(err_log_part.lstrip('2>>').strip())
            latter_part = latter_part[:err_log_start].strip()

        err_log_start = latter_part.find('2>')
        if err_log_start != -1:
            err_log_part = latter_part[err_log_start:].strip()
            self.set_error_log_file(err_log_part.lstrip('2>>').strip())
            latter_part = latter_part[:err_log_start].strip()

        # extract the log part
        log_start = latter_part.find('>')
        if log_start != -1:
            log_part = latter_part[log_start:].strip()
            self.set_log_file(log_part.lstrip('>').strip())
            latter_part = latter_part[:log_start].strip()

        log_start = latter_part.find('>>')
        if log_start != -1:
            log_part = latter_part[log_start:].strip()
            self.set_log_file(log_part.lstrip('>>').strip())
            latter_part = latter_part[:log_start].strip()

        # finally set the command to run
        self.set_command(latter_part)

    def render(self):
        """Creates a crontab string from all params passed"""
        cron_string = self.expression + ' ' + self.command

        if self.log_file:
            cron_string += ' >> ' + self.log_file

        if self.error_log_file:
            cron_string += ' 2>> ' + self.error_log_file

        if self.comments:
            cron_string += ' # ' + self.comments

        return cron_string

