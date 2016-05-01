import os
import pwd
import subprocess

class Crontab:

    def __init__(self, username=None, host=None):
        if not username:
            self.username = str(pwd.getpwuid(os.getuid()).pw_name)

        if host and '@' in host:
            self.host = host
        elif host:
            self.host = self.username + '@' + host
        else:
            self.host = None

        self.username_arg = "-u" + self.username

    def _run_command(self, arg, pre_cron=None):
        if self.host: # and self.host not in ['localhost', '127.0.0.1']: # <- uncomment this!
            if pre_cron:
                command_tuple = ("ssh", self.host, pre_cron, "crontab", arg)
            else:
                command_tuple = ("ssh", self.host, "crontab", arg)
        else:
            command_tuple = ("crontab", self.username_arg, arg)

        return subprocess.Popen(command_tuple, stdout=subprocess.PIPE)

    def list(self):
        """Get a list of all the crontabs for the user"""
        return self._run_command("-l")

    def remove(self):
        """Remove all crontabs for the current user"""
        return self._run_command("-r")

    def _install_remote(self, jobs):
        """Installs jobs on a remote machine"""
        pass

    def install(self, filepath):
        """Install a new crontab"""
        if not os.path.exists(filepath):
            raise FileNotFound("File doesn't exist: {}".format(filepath))

        return self._run_command(" {}".format(self.username, filepath))
