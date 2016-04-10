import os
import pwd
import subprocess

class Crontab:

    def __init__(self, username=None, host=None):
        """
        :param username: owner of the crontab
        """

        if not username:
            self.username = str(pwd.getpwuid(os.getuid()).pw_name)

        if host and '@' in host:
            self.host = host
        elif host:
            self.host = self.username + '@' + host
        else:
            self.host = None

        self.username_arg = "-u" + self.username

    def _run_command(self, arg):
        if self.host:
            # command_part = "ssh " + self.host + " "
            command_tuple = ("ssh", self.host, "crontab", arg)
        else:
            command_tuple = ("crontab", self.username_arg, arg)

        return subprocess.Popen(command_tuple, stdout=subprocess.PIPE)

    def list(self):
        """
        Get a list of all the crontabs for the user
        """
        return self._run_command("-l")

    def remove(self):
        """
        Remove all crontabs for the current user
        """
        return self._run_command("-r")

    def install(self, filepath):
        """
        Install a new crontab

        :param filepath: path to the file containing cron expressions
        """
        if not os.path.exists(filepath):
            raise FileNotFound("File doesn't exist: {}".format(filepath))

        return self._run_command("-i {}".format(self.username, filepath))
