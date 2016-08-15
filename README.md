# crony
crony is a tool that helps you manage crontabs that are present on your
local machine (as well as remote) right our of your terminal.

### Features

Let's say you want to list the cron jobs present on you local machine, with
crony all you need to do is:

    $ crony ls
    +----+--------------------+--------------+--------------+------------------+
    | ID |      Command       |  Expression  |   Log File   |    Error Log     |
    +----+--------------------+--------------+--------------+------------------+
    | 1  |   ls /tmp/*.csv    |  * * * * *   | /tmp/out.log | /tmp/err.out.log |
    | 2  | /tmp/createfile.sh | */6 * * * *  |              |                  |
    +----+--------------------+--------------+--------------+------------------+

Well this may not be impressive as you can achieve the same thing using the
default crontab command (crontab -l), but what if you want to list the cron jobs
present on a remote server, or better yet - a docker container that's running an
sshd daemon! With crony all you would need to do is:

    $ crony ls root@0.0.0.0:32768 
    +----+--------------------+--------------+--------------+------------------+
    | ID |      Command       |  Expression  |   Log File   |    Error Log     |
    +----+--------------------+--------------+--------------+------------------+
    | 1  | /tmp/createfile.sh | */10 * * * * |              |                  |
    +----+--------------------+--------------+--------------+------------------+

crony can copy crontabs across servers as well as delete remote cronjobs, but 
that won't be all. Keep watching this page as we build more features into crony.

### Installation

    git clone https://github.com/int3rlop3r/crony.git
    cd crony
    python setup.py install
