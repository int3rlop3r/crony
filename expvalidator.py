import re

MINUTE = 0
HOUR = 1
DAY_OF_MONTH = 2
MONTH = 3
DAY_OF_WEEK = 4

CRON_LIMITS = [59, 59, 31, 12, 8]
FIELD_NAMES = ['MINUTE', 'HOUR', 'DAY_OF_MONTH', 'MONTH', 'DAY_OF_WEEK']

# gets an integer value from a string
_get_int = lambda x: x.isdigit() and int(x)

def _validate_field(field_value, index):
    """Does the actual validation of the cron field """
    # fetch the value limit for the current field
    limit = CRON_LIMITS[index]

    if not field_value in ['*', '0']:
        for v in field_value.split(','):
            # fetch the number part from the string
            # eg: 50-3/5 will fetch only 50
            try:
                field_intval = int(v)
            except Exception:
                field_intval = int(re.search("\d*", v).group(0))

            if 0 > field_intval or field_intval > limit:
                raise AttributeError("Invalid value for {}: {}".format(FIELD_NAMES[index], v))

    return True

def validate_minute(field_value):
    """Validate the minute field"""
    return _validate_field(field_value, MINUTE)

def validate_hour(field_value):
    """Validate the hour field"""
    return _validate_field(field_value, HOUR)

def validate_day_of_month(field_value):
    """Validate the day of month field"""
    return _validate_field(field_value, DAY_OF_MONTH)

def validate_month(field_value):
    """Validate the month field"""
    return _validate_field(field_value, MONTH)
 

def validate_day_of_week(field_value):
    """Validate the day of week field"""
    return _validate_field(field_value, DAY_OF_WEEK)

def validate(expression):
    """Validate all the fields of the cron expression"""
    if isinstance(expression, str):
        expression = expression.split()

    for index, expression_part in enumerate(expression):
        _validate_field(expression_part, index)
