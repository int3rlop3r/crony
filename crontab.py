import os
import pwd
import subprocess

class Crontab:

    def __init__(self, username=None):
        """
        :param username: owner of the crontab
        """
        if not username:
            self.username_arg = "-u " + str(pwd.getpwuid(os.getuid()).pw_name)

    def _run_command(self, arg):
        return subprocess.Popen(("crontab", arg),
                                stdout=subprocess.PIPE)

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
