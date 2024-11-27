
def get_utilization(current, total):
  util = 0
  if current and total:
    util = 1 - ((total - current) / total)
    if util < 0:
      util = 0
    elif util > 1:
      util = 1
  return util

def get_cpu_util(interval, cur, prev, freq_per_core, n_cores, cores_considered=0):
  """get the total cpu utilization

  Args:
    interval (float): interval time
    cur (object): is the current metric object
    prev (object): is the previous metric object
    freq_per_core (int): is the frequency of one core
    n_cores (int): number of cores in the host
    cores_considered (int, optional): number of cores to perform the calculation. Defaults to 0.

  Returns:
    float: value of cpu utilization
  """
  if interval > 0:
    # get cpu cores usage
    cores_mean = (cur - prev) / interval / 1000
    if cores_considered == 0:
      total = freq_per_core * n_cores
    elif cores_considered > 0:
      total = freq_per_core * cores_considered
    current = cores_mean * freq_per_core
    usage = get_utilization(current, total)
  else:
    usage = 0
  return usage

def get_net(interval, cur, prev):
  """get network calculation

  Args:
    interval (float): interval time as seconds
    cur (int): current network value
    prev (int): previous network value

  Returns:
    float: calculated network value
  """
  net = 0
  if interval > 0:
    net = (cur - prev) / (interval / 1000000000)
  return net