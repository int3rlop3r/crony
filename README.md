# Crony
Crony is a tool that helps you manage all your crontabs in one place.

### Features

List jobs present on your local machine:

    $ crony ls
    +----+--------------------+--------------+--------------+------------------+
    | ID |      Command       |  Expression  |   Log File   |    Error Log     |
    +----+--------------------+--------------+--------------+------------------+
    | 1  |   ls /tmp/*.csv    |  * * * * *   | /tmp/out.log | /tmp/err.out.log |
    | 2  | /tmp/createfile.sh | */6 * * * *  |              |                  |
    +----+--------------------+--------------+--------------+------------------+

List jobs on a remote machine:

    $ crony ls root@localhost:32768 
    root@localhost's password: 
    +----+--------------+------------+---------------+-------------------+
    | ID |   Command    | Expression |    Log File   |     Error Log     |
    +----+--------------+------------+---------------+-------------------+
    | 1  | /tmp/blah.sh | 58 * * * * | /tmp/blah.log | /tmp/blah.err.log |
    +----+--------------+------------+---------------+-------------------+

Crony can also copy and delete jobs across servers.

Missing a feature? - Add an Issue! (;

### Installation

    git clone https://github.com/int3rlop3r/crony.git
    cd crony
    python setup.py install
