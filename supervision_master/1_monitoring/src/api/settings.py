from .constants import LH_ID, LH_PAIR
from multiprocessing import Manager

hosts_list = [
    {'id': LH_ID,
    'name': 'localhost',
    'location': 'http://' + LH_PAIR},
]
active_hosts_list = []

active_solutions_list = Manager().dict()
aggregates_flag = None