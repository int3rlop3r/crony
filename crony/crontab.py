import os
import subprocess

class Command(object):

    def __init__(self, args, shell=False):
        self.command_args = args
        self.shell = shell

    @property
    def command(self):
        """Display the command as a string"""
        return " ".join(self.command_args)

    def run(self):
        """Execute the command and pipes the output to pipe"""
        return subprocess.Popen(
                self.command_args, 
                stdout=subprocess.PIPE, 
                shell=self.shell)

class CommandBuilder(object):
    """Builds a Command object using the environment params"""

    def __init__(self, hostname=None, username=None, port=22, cronuser=None):

        self.hostname = hostname
        self.port = str(port)

        if username:
            self.username = username
            self.is_localhost = False
            self.uri = username + '@' + self.hostname

        # not supported yet!!
        if cronuser:
            self.cronuser_arg = "-u" + cronuser
        else:
            self.cronuser_arg = None

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        if not hostname:
            hostname = 'localhost'

        if hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
            self.uri = 'localhost'
            self.is_localhost = True
        else:
            self.uri = hostname
            self.is_localhost = False

        self._hostname = hostname

    def buildcommand(self, args=None, command_args=None, shell=False):
        crontab_command = ["crontab"]
        ssh_command = ["ssh", "-p", self.port, self.uri]

        if not command_args:
            command_args = crontab_command + args

        if not self.is_localhost:
            command_args = ssh_command + command_args

        return Command(args=command_args, shell=shell)

    def _edit(self, command_args):
        if self.is_localhost:
            shell = True # <- for local
        else:
            shell = False  # <- for remote
        return self.buildcommand(command_args=command_args, shell=shell)

    def list(self):
        return self.buildcommand(["-l"])

    def remove(self):
        return self.buildcommand(["-r"])

    def append(self, jobs):
        return self._edit(["(crontab -l 2> /dev/null; "
                           "printf \"" + jobs + "\") "
                           "| crontab -"])

    def install(self, jobs):
        return self._edit(["(printf \"" + jobs + "\") | crontab -"])

class Crontab:

    def __init__(self, **kwargs):
        self.debug = kwargs.get('debug', False)
        self.cbuilder = CommandBuilder(**kwargs)

    def list(self):
        """Get a list of all the crontabs for the user"""
        return self.cbuilder.list().run()

    def remove(self):
        """Remove all crontabs for the current user"""
        return self.cbuilder.remove().run()

    def append(self, jobs):
        """Append a crontab"""
        return self.cbuilder.append(jobs).run()

    def install(self, jobs):
        """Install a new crontab overwriting the old one"""
        return self.cbuilder.install(jobs).run()

