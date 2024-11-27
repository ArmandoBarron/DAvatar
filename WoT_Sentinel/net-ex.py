import psutil
import time
def check_speeds():
    rs = {}
    for net_name,stats in psutil.net_if_stats().items():
        if type(stats) is tuple or not stats.isup:
            continue
        rs[net_name] = stats.speed
    return rs
def snapshoot():
    rs = {}
    for net_name,stats in psutil.net_io_counters(pernic=True).items():
        rs[net_name] = stats.bytes_recv
    return rs

nets = check_speeds()
while True:
    print ('###########################')
    snap_prev = snapshoot()
    time.sleep(1)
    snap_now = snapshoot()

    print(snap_prev)
    print(snap_now)
    for net_name,speed in nets.items():
        recv_prev = snap_prev[net_name]
        recv_now = snap_now[net_name]
        print(recv_prev)
        print(recv_now)
        print(speed)
        rate = (recv_now-recv_prev)/(speed*1024*1024/8)
        print ('name: ' + str(net_name) + " - rate: " + str(rate*100))