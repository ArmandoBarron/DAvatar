from datetime import datetime

def get_timestamp(current):
    """Trim timestamp string of variable lenght up to 26 characters.
    The timestamp is in format RFC 3339

    Args:
        current (str): string timestamp of variable lenght

    Returns:
        str: string timestamp with lenght of 26
    """
    # let frac_sec up to 6 digits 
    if len(current) == 30:
        current = current[:-4]
    elif len(current) == 29:
        current = current[:-3]
    elif len(current) == 28:
        current = current[:-2]

    if current[-1] != 'Z':
        current = current + 'Z'
    return current

def get_interval(current, previous):
    """Gets the length of the interval in nanoseconds.
    The Timestamp type is encoded as a string in the
    [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) format. That is, the
    format is "{year}-{month}-{day}T{hour}:{min}:{sec}[.{frac_sec}]Z"
    where {year} is always expressed using four digits while {month}, {day},
    {hour}, {min}, and {sec} are zero-padded to two digits each. The fractional
    seconds, which can go up to 9 digits. The "Z" suffix indicates the timezone ("UTC"); 
    the timezone is required. 
    In Python, a standard `datetime.datetime` object can be converted to 
    this format using [`strftime`] with the time format spec '%Y-%m-%dT%H:%M:%S.%fZ'.

    Args:
        current (object): is the current metric object
        previous (object): is the previous metric object

    Returns:
        float: the time interval between current and previous timestamps
    """
    current = get_timestamp(current)
    previous = get_timestamp(previous)

    # get datetime up to microseconds*
    cur = parse_RFC3339_str_to_datetime(current)
    prev = parse_RFC3339_str_to_datetime(previous)

    # ms (millisecond 10^-3) -> ns (nanosecond 10^-9).
    return (cur.timestamp() - prev.timestamp()) * 1000000

def parse_RFC3339_str_to_datetime(date_time):
    return datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S.%fZ')

def parse_RFC3339_datetime_to_str(date_time):
    return datetime.strftime(date_time, '%Y-%m-%dT%H:%M:%S.%fZ')

