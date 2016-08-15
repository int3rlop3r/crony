import os
import subprocess

class Crontab:

    def __init__(self, hostname, username=None, port=22, cronuser=None, debug=False):
        localhostnames = ['localhost', '127.0.0.1', '0.0.0.0']

        self.port = str(port)
        self.debug = debug
        self.cronuser_arg = None
        self.is_localhost = False
        self.hostname = hostname
        self.uri = hostname

        if hostname in localhostnames:
            self.uri = None
            self.is_localhost = True

        if username:
            self.is_localhost = False
            self.username = username
            self.uri = self.username + '@' + self.hostname

        if cronuser: # not supported yet!!
            self.cronuser_arg = "-u" + self.cronuser

    def _run_command(self, arg=None, command_args=None, shell=False, debug=False):
        if not command_args:
            if self.is_localhost and self.cronuser_arg:
                # interact with another user's crontab
                command_args = ("crontab", self.cronuser_arg, arg)
            elif self.is_localhost:
                command_args = ("crontab", arg)
            else:
                command_args = ("ssh", "-p", self.port, self.uri, "crontab", arg)

        if debug:
            print("Debug msg:")
            print(command_args)

        # execute the command and pipe the output to stdout
        return subprocess.Popen(command_args, stdout=subprocess.PIPE, shell=shell)

    def list(self):
        """Get a list of all the crontabs for the user"""
        return self._run_command("-l", debug=self.debug)

    def remove(self):
        """Remove all crontabs for the current user"""
        return self._run_command("-r")

    def append(self, s_jobs):
        """Append a crontab"""
        if self.is_localhost:
            command_args = "(crontab -l 2> /dev/null; printf \"{}\") | crontab -".format(s_jobs)
            shell=True
        else:
            command_args = ("ssh", "-p", self.port, self.uri, "(crontab -l 2> /dev/null; printf \"{}\") | crontab -".format(s_jobs))
            shell=False

        return self._run_command(command_args=command_args, shell=shell, debug=self.debug)

    def copy_new(self, s_jobs):
        """Install a new crontab overwriting the old one"""
        if self.is_localhost:
            command_args = "(printf \"{}\") | crontab -".format(s_jobs)
            shell=True
        else:
            command_args = ("ssh", "-p", self.port, self.uri, "(printf \"{}\") | crontab -".format(s_jobs))
            shell=False

        return self._run_command(command_args=command_args, shell=shell, debug=self.debug)

