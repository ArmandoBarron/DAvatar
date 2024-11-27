from .datetime_handler import get_interval

def get_util(total, current):
    return 1 - ( (total - current) / total)

def get_cpu_util(freq_per_core, n_cores, cur, prev):
    """get the total cpu utilization

    Args:
        freq_per_core (int): is the frequency of one core
        n_cores (int): is the number of cores
        cur (object): is the current metric object
        prev (object): is the previous metric object

    Returns:
        float: value of cpu utilization
    """
    intervals = get_interval(cur.get('timestamp'), prev.get('timestamp'))
    if intervals > 0.0:
        # get cpu cores usage
        cores_mean = (cur.get('cpu').get('usage_total') - prev.get('cpu').get('usage_total')) / intervals / 1000
        total = freq_per_core * n_cores
        current = cores_mean * freq_per_core
        usage = get_util(total, current)
    else:
        usage = 0
    return usage

def get_mem_util(total, cur):
    usage = get_util(total, cur.get('memory').get('usage'))
    return usage

def get_fs_util(total, cur):
    sum_filesystem = 0
    t_fs2 = 0
    for elem in cur.get('filesystem'):
        sum_filesystem += elem.get('usage')
        t_fs2 += elem.get('capacity')
    # can be used total or t_fs2
    usage = get_util(t_fs2, sum_filesystem)
    return usage

def get_net_util(total, cur, prev):
    cur_net = cur.get('network')
    prev_net = prev.get('network')
    util = 0
    if type(cur_net) is list and type(prev_net) is list:

        c_rtx = 0
        p_rtx = 0
        # zip returns a tuple with one element of each iterable in
        for c,p in zip(cur_net,prev_net): # for big lists use itertools.izip
            
            c_rtx += c.get('rx_bytes') + c.get('tx_bytes')
            p_rtx += p.get('rx_bytes') + p.get('tx_bytes')
        
        curr = c_rtx - p_rtx # added by the cumulative tendency showed in experiments
        
        # to handle with util and without util
        # currently using without
        if total:
            util = get_util(total, curr)
        else:
            util = curr
    return util

def get_fs(cur):
    sum_filesystem = 0
    if cur.get('filesystem'):
        for elem in cur.get('filesystem'):
            sum_filesystem += elem.get('usage')
    return sum_filesystem

def get_net(cur):
    cur_net = cur.get('network')
    sum_net = 0
    if cur_net and type(cur_net) is list:
        for c in cur_net:
            # added by the cumulative tendency showed in experiments
            sum_net += c.get('rx_bytes') + c.get('tx_bytes')
    return sum_net