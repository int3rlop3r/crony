import unittest
from crony.builder import Job, Jobs

class TestJob(unittest.TestCase):

    def test_setters_and_getters(self):
        job = Job()
        job.expression = '* * * * *'
        job.command = 'ls'
        job.log_file = 'out.log'
        job.error_log_file = 'err_out.log'
        job.comments = 'Hey this is a comment'

        # test expression part
        self.assertEquals(job.minute, '*')
        self.assertEquals(job.hour, '*')
        self.assertEquals(job.day_of_month, '*')
        self.assertEquals(job.month, '*')
        self.assertEquals(job.day_of_week, '*')

        # test job part
        self.assertEquals(job.command, 'ls')
        self.assertEquals(job.comments, 'Hey this is a comment')
        self.assertEquals(job.log_file, 'out.log')
        self.assertEquals(job.error_log_file, 'err_out.log')

    def test_parse_job_line(self):
        line = "* * * * * ls >> out.log 2>> err_out.log"
        job = Job()
        job.line = line

        # test expression part
        self.assertEquals(job.expression, '* * * * *')
        self.assertEquals(job.minute, '*')
        self.assertEquals(job.hour, '*')
        self.assertEquals(job.day_of_month, '*')
        self.assertEquals(job.month, '*')
        self.assertEquals(job.day_of_week, '*')

        # test job part
        self.assertEquals(job.command, 'ls')
        self.assertEquals(job.log_file, 'out.log')
        self.assertEquals(job.error_log_file, 'err_out.log')
        self.assertEquals(job.comments, '')

    def test_job_line(self):
        line = "* * * * * ls >> out.log"
        job = Job(line)
        self.assertEquals(job.line, line)
        self.assertEquals(str(job), line)

class TestJobs(unittest.TestCase):

    def setUp(self):
        self.job1 = Job("* * * * * job1")
        self.job2 = Job("* * * * * job2")
        self.job3 = Job("* * * * * job3")
        self.job4 = Job("* * * * * job4")
        self.job5 = Job("* * * * * job5")
        self.job6 = Job("@reboot job5")

    def test_add(self):
        # test jobs from constructor
        jobs = Jobs([self.job1, self.job2, self.job3])
        self.assertEquals(len(jobs), 3)

        # test add method
        jobs.add(self.job4)
        jobs.add(self.job5)
        self.assertEquals(len(jobs), 5)

        # test adding an invalid job
        with self.assertRaises(AttributeError):
            jobs.add('invalidobject')

        jobs.clear_all()

    def test_get(self):
        jobs = Jobs([
            self.job1,
            self.job2,
            self.job3,
            self.job4,
            self.job5,
            self.job6,
        ])

        self.assertEquals(self.job1, jobs.get(1))
        self.assertEquals(self.job2, jobs.get(2))
        self.assertEquals(self.job3, jobs.get(3))
        self.assertEquals(self.job4, jobs.get(4))
        self.assertEquals(self.job5, jobs.get(5))
        self.assertEquals(self.job6, jobs.get(6))

    def test_merge(self):
        jobsa = Jobs([self.job1, self.job2, self.job3])
        jobsb = Jobs([self.job4, self.job5, self.job6])

        jobsa.merge(jobsb)
        self.assertEquals(self.job1, jobsa.get(1))
        self.assertEquals(self.job2, jobsa.get(2))
        self.assertEquals(self.job3, jobsa.get(3))
        self.assertEquals(self.job4, jobsa.get(4))
        self.assertEquals(self.job5, jobsa.get(5))
        self.assertEquals(self.job6, jobsa.get(6))

    def test_in_ids(self):
        jobs = Jobs([
            self.job1,
            self.job2,
            self.job3,
            self.job4,
            self.job5,
            self.job6,
        ])

        subjobs = jobs.in_ids([1, 2, 6])
        self.assertEquals(self.job1, subjobs.get(1))
        self.assertEquals(self.job2, subjobs.get(2))
        self.assertEquals(self.job6, subjobs.get(3))

    def test_all(self):
        joblist = [
            self.job1,
            self.job2,
            self.job3,
            self.job4,
            self.job5,
            self.job6,
        ]

        jobs = Jobs(joblist)
        self.assertEquals(joblist, jobs.all())

    def test_remove(self):
        joblist = [
            self.job1,
            self.job2,
            self.job3,
            self.job4,
            self.job5,
            self.job6,
        ]

        jobs = Jobs(joblist[:])
        joblist.remove(self.job1) #remove job1
        jobs.remove(self.job1)
        self.assertEquals(jobs.all(), joblist)

    def test_clear_all(self):
        jobs = Jobs([self.job1, self.job2, self.job3])
        jobs.clear_all()
        self.assertEquals(len(jobs), 0)
    
    def test_iterator(self):
        joblist = [
            self.job1,
            self.job2,
            self.job3,
            self.job4,
            self.job5,
            self.job6,
        ]

        jobs = Jobs(joblist[:])
        for index, job in enumerate(jobs):
            self.assertEquals(job.line, joblist[index].line)

