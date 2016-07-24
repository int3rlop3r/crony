import os
import utils
import subprocess

class Crontab:

    def __init__(self, username=None, remote_server=None, port=22, debug=False):
        self.is_localhost = False
        self.port = str(port)
        self.debug = debug
        localhostnames = ['localhost', '127.0.0.1']

        if not username:
            self.username = utils.get_username()

        if remote_server and '@' in remote_server:
            self.uri = remote_server
            r_pcs = remote_server.split("@")

            self.username = r_pcs[0]
            self.hostname = r_pcs[1]

            if self.hostname in localhostnames:
                self.is_localhost = True

        elif remote_server:
            self.uri = self.username + '@' + remote_server
            self.hostname = remote_server

            if remote_server in localhostnames:
                self.is_localhost = True
        else:
            # username already set above!
            self.uri = None
            self.is_localhost = True
            self.hostname = 'localhost'

        self.username_arg = "-u" + self.username

    def _run_command(self, arg=None, command_args=None, shell=False, debug=False):
        if not command_args:
            if self.is_localhost: # and self.uri not in ['localhost', '127.0.0.1']: # <- uncomment this!
                command_args = ("crontab", self.username_arg, arg)
            else:
                command_args = ("ssh", "-p", self.port, self.uri, "crontab", arg)

        if debug:
            print(command_args)

        # execute the command and pipe the output to stdout
        return subprocess.Popen(command_args, stdout=subprocess.PIPE, shell=shell)

    def list(self):
        """Get a list of all the crontabs for the user"""
        return self._run_command("-l")

    def remove(self):
        """Remove all crontabs for the current user"""
        return self._run_command("-r")

    def append(self, s_jobs):
        """Append a crontab"""
        if self.is_localhost:
            command_args = ("(crontab -l 2> /dev/null; printf \"{}\") | crontab -".format(s_jobs))
        else:
            command_args = ("ssh", "-p", self.port, self.uri, "(crontab -l 2> /dev/null; printf \"{}\") | crontab -".format(s_jobs))

        return self._run_command(command_args=command_args, debug=self.debug)

    def copy_new(self, s_jobs):
        """Install a new crontab overwriting the old one"""
        if self.is_localhost:
            command_args = ( "(printf \"{}\") | crontab -".format(s_jobs))
        else:
            command_args = ( "ssh", "-p", self.port, self.uri, "(printf \"{}\") | crontab -".format(s_jobs))

        return self._run_command(command_args=command_args, debug=self.debug)

