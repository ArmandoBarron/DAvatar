from datetime import datetime

def parse_RFC3339_str_to_datetime(date_time):
    return datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S.%fZ')

def parse_RFC3339_datetime_to_str(date_time):
    return datetime.strftime(date_time, '%Y-%m-%dT%H:%M:%S.%fZ')
