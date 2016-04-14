import os
import re
from prettytable import PrettyTable

def horizontal_table(jobs):
    """Displays jobs in a horizontal table"""
    id_counter = 1
    t = PrettyTable(("ID", "Command", "Expression", "Log File", "Error Log"))

    def chop_line(line):
        line_size = len(line)
        script_name = os.path.basename(line)

        if line_size > 50:
            line = re.sub("(.{50})", "\\1\n", line, 0, re.DOTALL)

        return line

    for job in jobs:
        t.add_row(( id_counter, 
                    chop_line(job.command),
                    chop_line(job.expression), 
                    chop_line(job.log_file),
                    chop_line(job.error_log_file) ))
        id_counter += 1

    return t
