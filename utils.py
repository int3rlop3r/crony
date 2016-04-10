import click

def parse_range_callback(ctx, param, value):
    """
    Callback function that parses the range entered
    from the commandline
    """
    try:
        return parse_range(value)
    except (ValueError, TypeError) as ve:
        raise click.BadParameter(str(ve))

def parse_range(value):
    """
    Parses the range entered as string and returns a set
    eg:
        The string 1,2,3,4 would be { 1, 2, 3, 4 }
        1-5 would be { 1, 2, 3, 4, 5 }
        1,2,4-6 would be {1, 2, 4, 5, 6}
    """
    cronids = set()
    ids = value.split(',')
    for cron_id in ids:
        if '-' in cron_id:
            cron_id_pcs = cron_id.split('-')

            # this has to be 2, eg: 1-5, not 1-5-8, etc.
            if len(cron_id_pcs) != 2:
                raise ValueError("Invalid range: %s" % cron_id)

            start_idx = int(cron_id_pcs[0])
            end_idx = int(cron_id_pcs[1]) + 1

            if start_idx < 0 or end_idx < start_idx:
                raise ValueError("Invalid range: %s" % cron_id)

            for cid in range(start_idx, end_idx):
                cronids.add(int(cid))
        else:
            cronids.add(int(cron_id))
    return cronids
